import datetime

from django.http import HttpResponse
from django.utils import timezone

from .models import *
from profiles.models import Profiles
from main.tasks import create_car_info_celery
import json
from .utils import get_token_by_invoice_id
from main.tasks import send_mail_


def on_one_time_complete_callback(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=404)
    profile = Profiles.object.get(email=request.user.email)
    data = json.loads(request.body)
    try:
        invoice_id = data['invoice_id']
        type = data['type']
        number = data['number']
        user = data['user']
        success = data['results']['success']
        order = Order.objects.get(invoice_id=invoice_id, profile=profile)
    except:
        return HttpResponse(status=404)
    if not success:
        return HttpResponse(status=400)
    if order.is_report_ready:
        return HttpResponse(status=400)
    if request.user.email != user:
        return HttpResponse(status=400)
    host = 'reportcar.ru'
    protocol = 'https://'
    create_car_info_celery.delay(protocol, host, user, type, number)
    order.status = True
    order.is_report_ready = True
    order.save()
    return HttpResponse(status=200)


def on_recurrent_complete_callback(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=404)
    data = json.loads(request.body)
    try:
        success = data['results']['success']
        email = data['results']['email']
    except:
        return HttpResponse(status=404)
    if request.user.email != email:
        return HttpResponse(status=404)
    if not success:
        return HttpResponse(status=404)
    profile = Profiles.object.get(email=request.user.email)
    rate_type = RateType.objects.get(title=data['options']['data']['type'])
    card_token = get_token_by_invoice_id(data['options']['invoiceId'])
    if card_token is None:
        return HttpResponse(status=404)
    payment_method = PaymentMethod.objects.create(
        profile=profile,
        encrypted_token=card_token
    )
    subscribe = Subscribe.objects.create(
        profile=profile,
        rate_type=rate_type,
        process='0',
        status='1',
        reports_counter=3,
        payment_method=payment_method,
        process_date_expired=timezone.now()+datetime.timedelta(3)
    )
    RecurrentOrder.objects.create(
        profile=profile,
        subscribe=subscribe,
        invoice_id=data['options']['invoiceId'],
        payment_purpose=0,
        status=True
    )
    send_mail_.delay(subject='Подписка успешно оформлена',
                     text=f'Подписка на тариф {rate_type.title} успешно оформлена.\n'
                          f'Вам начислено 3 отчета на 3 дня, подписка автоматически активируется по истечении 3-х дней или раньше'
                          f', если вы истратите 3 отчета.',
                     email=email)
    return HttpResponse(status=200)

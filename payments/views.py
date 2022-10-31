import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from main.tasks import create_car_info_celery
from .models import *
from profiles.models import Profiles
from yookassa import Payment
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


def get_ip_address(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
def pay_callback(request):
    ip_ = get_ip_address(request)
    print(f'ip from {ip_}')
    data = json.loads(request.body)
    try:
        payment_model = OneTimePayment.objects.get(payment_id=data['object']['id'])
    except ObjectDoesNotExist:
        payment_model = SubscribePayment.objects.get(payment_id=data['object']['id'])
    payment = Payment.find_one(payment_model.payment_id)
    payment_data = json.loads(payment.json())
    if payment_data['metadata']['payment'] == 'one-time':
        one_time_pay_handler(payment_data, payment_model)
        return HttpResponse(status=200)
    if payment_data['metadata']['payment'] == 'subscribe':
        subscribe_pay_handler(payment_data, payment_model)
        return HttpResponse(status=200)
    return HttpResponse(status=200)


def one_time_pay_handler(payment_data, payment_model):
    payment_model.status = payment_data['status']
    payment_model.paid = payment_data['paid']
    payment_model.save()
    protocol = 'https://'
    host = 'reportcar.ru'
    create_car_info_celery.delay(protocol, host, payment_model.profile.email,
                                 payment_data['metadata']['type'], payment_data['metadata']['number'])
    return HttpResponse(status=200)


def subscribe_pay_handler(payment, payment_model):
    payment_data = json.loads(payment.json())
    payment_model.status = payment_data['status']
    payment_model.paid = payment_data['paid']
    payment_model.save()
    payment_method = SubscribePaymentMethod.objects.create(
        profile=payment_model.profile,
        payment_method_id=payment_data['payment_method']['id'],
        saved=payment_data['payment_method']['saved']
    )
    RateSubscribe.objects.create(
        payment_method=payment_method,
        rate_type=RateType.objects.get(title=payment_data['metadata']['typename']),
        report_counter=3,
        step='start',
        step_date_expired=timezone.localdate() + timedelta(3)
    )
    return HttpResponse(status=200)


def pay_redirect(request):
    return redirect(reverse('lk') +
                    f'?redirect=success')

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


@csrf_exempt
def pay_callback(request):
    data = json.loads(request.body)
    if data['metadata']['payment'] == 'one-time':
        one_time_pay_handler(data)
    if data['metadata']['payment'] == 'subscribe':
        subscribe_pay_handler(data)


def one_time_pay_handler(data):
    payment_model = OneTimePayment.objects.get(payment_id=data['object']['id'])
    payment = Payment.find_one(payment_model.payment_id)
    payment_data = json.loads(payment.json())
    payment_model.status = payment_data['status']
    payment_model.paid = payment_data['paid']
    payment_model.save()
    protocol = 'https://'
    host = 'reportcar.ru/'
    create_car_info_celery.delay(protocol, host, payment_model.profile.email,
                                 payment_data['metadata']['type'], payment_data['metadata']['number'])
    return HttpResponse(status=200)


def subscribe_pay_handler(data):
    payment_model = SubscribePayment.objects.get(payment_id=data['object']['id'])
    payment = Payment.find_one(payment_model.payment_id)
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

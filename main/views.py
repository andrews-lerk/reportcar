import time
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone

from .forms import *
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
import json
from profiles.models import Profiles
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ObjectDoesNotExist
from reports.utils import get_restrict_car_info
from config.settings import EMAIL_HOST_USER
from reports.models import Vehicle, VinDecode, VehiclePeriods, Dtp, \
    Restrict, Wanted, Pledges, Reviews, Taxi, \
    CustomsClearance, RNISRegister, Osago, DiagnosticsActive, DiagnosticsExpired, Image
from .tasks import create_car_info_celery, send_mail_
from .models import FAQ, ReportsViewCounter
from payments.models import RateType, Order
from payments.utils import random_invoice_id, activate_subscribe
from payments.models import *


def index(request):
    if request.method == 'POST':
        return redirect(reverse('check') +
                        f'?type={request.POST.get("select")}' +
                        f'&number={request.POST.get("forminnumber")}')
    counter = ReportsViewCounter.objects.all().first().value
    return render(request, 'index.html', {'counter': counter})


def pricing(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            type = data['type']
        except:
            return HttpResponse(status=404)
        try:
            rates = RateType.objects.get(title=type)
        except:
            return HttpResponse(status=404)
        subscribe = Subscribe.objects.filter(profile=Profiles.object.get(email=request.user.email))
        if len(subscribe) > 0:
            subscribe = True
        else:
            subscribe = False
        response = {
            'type': type,
            'startPrice': rates.start_price,
            'user': request.user.email,
            'invoiceId': random_invoice_id(),
            'subscribe': subscribe
        }
        return JsonResponse(response)
    rates = RateType.objects.all()
    context = {
        'rates': rates,
        'time': timezone.now()
    }
    return render(request, 'pricing.html', context)


def faq(request):
    faq = FAQ.objects.all()
    return render(request, 'faq.html', {'faq': faq})


def politics(request):
    return render(request, 'politics.html')


def tariffs(request):
    return render(request, 'tariffs.html')


def offer(request):
    return render(request, 'offer.html')


def report_detail(request, key):
    report = Vehicle.objects.get(key=key)
    decode = VinDecode.objects.get(vehicle=report)
    osago = Osago.objects.get(vehicle=report)

    periods = VehiclePeriods.objects.filter(vehicle=report)

    img = Image.objects.filter(vehicle=report)

    if len(img) == 0:
        img = False

    active = DiagnosticsActive.objects.filter(vehicle=report)
    if len(active) == 0:
        active = False
    else:
        active = active.first()

    expired = DiagnosticsExpired.objects.filter(vehicle=report)
    if len(expired) == 0:
        expired = False

    dtp = Dtp.objects.filter(vehicle=report)
    if len(dtp) == 0:
        dtp = False

    restrict = Restrict.objects.filter(vehicle=report)
    if len(restrict) == 0:
        restrict = False

    wanted = Wanted.objects.filter(vehicle=report)
    if len(wanted) == 0:
        wanted = False

    pledges = Pledges.objects.filter(vehicle=report)
    if len(pledges) == 0:
        pledges = False

    reviews = Reviews.objects.filter(vehicle=report)
    if len(reviews) == 0:
        reviews = False

    taxi = Taxi.objects.filter(vehicle=report)
    if len(taxi) == 0:
        taxi = False

    customs = CustomsClearance.objects.filter(vehicle=report)
    if len(customs) == 0:
        customs = False

    rnis = RNISRegister.objects.filter(vehicle=report)
    if len(rnis) == 0:
        rnis = False

    context = {
        'report': report,
        'decode': decode,
        'periods': periods,
        'dtp': dtp,
        'restrict': restrict,
        'wanted': wanted,
        'pledges': pledges,
        'reviews': reviews,
        'taxi': taxi,
        'customs': customs,
        'rnis': rnis,
        'osago': osago,
        'expired': expired,
        'active': active,
        'img': img
    }
    return render(request, 'reports/report.html', context)


def login_view(request):
    form = AuthForm()
    if request.method == "POST":
        data = json.loads(request.body)
        get_or_create_user(data['email'])
        return JsonResponse({'status': 'ok'})
    context = {
        'form': form,
    }
    return render(request, 'auth/login.html', context)


def get_or_create_user(email):
    password = Profiles.object.make_random_password(length=6, allowed_chars='0123456789')
    message = f'{password} - ваш код подтверждения для сайта reportcar.ru'
    send_mail_.delay(subject='Код подтверждения',
                     text=message,
                     email=email)
    try:
        user = Profiles.object.get(email=email)
        user.set_password(password)
        user.save()
        return user
    except ObjectDoesNotExist:
        user = Profiles.object.create_user(email=email, password=password)
        return user


def auth(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        passw = data['pass']
        user = authenticate(request=request, email=email,
                            password=passw)
        if user is None:
            return HttpResponse(status=400)
        login(request, user)
        return HttpResponse(status=200)
    return HttpResponse(status=400)


def pay_auth(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            data = json.loads(request.body)
            try:
                email = data['email']
                passw = data['pass']
            except:
                return HttpResponse(status=404)
            user = authenticate(request=request, email=email,
                                password=passw)
            if user is None:
                return HttpResponse(status=404)
            login(request, user)
        invoice_id = random_invoice_id()
        Order.objects.create(
            profile=Profiles.object.get(email=request.user.email),
            invoice_id=invoice_id
        )
        return JsonResponse({'user': request.user.email, 'invoice_id': invoice_id})
    return HttpResponse(status=400)


def logout_(request):
    logout(request)
    return redirect(index)


def check_car(request):
    type = request.GET.get('type')
    if type == 'None':
        type = 'GOS'
    number = request.GET.get('number')
    price = 99
    subscribe = Subscribe.objects.filter(profile=Profiles.object.get(email=request.user.email))
    if len(subscribe) == 1:
        subscribe = subscribe.first()
        if subscribe.process == "0" and subscribe.reports_counter == 1 and subscribe.status != '-1':
            create_car_info_celery.delay('https://', 'reportcar.ru', request.user.email, type, number)
            print('activation subscribe')
            activate_subscribe(subscribe)
            return redirect(reverse('lk') + '?redirect=success')
        if subscribe.reports_counter > 0 and subscribe.status != '-1':
            create_car_info_celery.delay('https://', 'reportcar.ru', request.user.email, type, number)
            subscribe.reports_counter -= 1
            subscribe.save()
            print('-1 report')
            return redirect(reverse('lk') + '?redirect=success')
        else:
            price = 59 if subscribe.status == '1' else 99
    form = AuthForm()
    context = {
        'form': form,
        'type': type,
        'number': number,
        'price': price
    }
    return render(request, 'reports/restrict_report.html', context)


def get_restrict_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        type = data['type']
        number = data['number']
        result = get_restrict_car_info(type, number)
        try:
            message = result['message']
            response = {'message': message, 'car': False}
        except:
            model = result['model']
            color = result['color']
            year = result['year']
            response = {
                'model': model,
                'color': color,
                'year': year,
                'car': True
            }
        return JsonResponse(response)


@login_required()
def lk(request):
    if request.method == 'POST':
        return redirect(reverse('check') +
                        f'?type={request.POST.get("select")}' +
                        f'&number={request.POST.get("forminnumber")}')
    reports = list(Vehicle.objects.filter(profile=request.user))
    reports.reverse()
    reports = reports[:3]
    try:
        subscribe = Subscribe.objects.get(profile=Profiles.object.get(email=request.user.email))
    except:
        subscribe = False
    context = {
        'reports': reports,
        'subscribe': subscribe
    }

    try:
        r = request.GET['redirect']
        context['redirect'] = r
    except:
        pass
    return render(request, 'lk.html', context)


@login_required()
def reports_list(request):
    reports = list(Vehicle.objects.filter(profile=request.user))
    reports.reverse()

    context = {
        'reports': reports
    }
    return render(request, 'reports/reports_list.html', context)


@login_required()
def remove_subscribe(request):
    subscribe = Subscribe.objects.get(profile=Profiles.object.get(email=request.user.email))
    subscribe.payment_method.delete()
    subscribe.delete()
    return redirect(lk)

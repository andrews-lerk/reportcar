import time
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import *
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
import json
from profiles.models import Profiles
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ObjectDoesNotExist
from reports.utils import get_restrict_car_info
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from reports.models import Vehicle, VinDecode, VehiclePeriods, Dtp, \
    Restrict, Wanted, Pledges, Reviews, Taxi, \
    CustomsClearance, RNISRegister, Osago, DiagnosticsActive, DiagnosticsExpired, Image
from .tasks import create_car_info_celery
from .models import FAQ, ReportsViewCounter


def index(request):
    if request.method == 'POST':
        return redirect(reverse('check') +
                        f'?type={request.POST.get("select")}' +
                        f'&number={request.POST.get("forminnumber")}')
    counter = ReportsViewCounter.objects.all().first().value
    return render(request, 'index.html', {'counter': counter})


def pricing(request):
    return render(request, 'pricing.html')


def faq(request):
    faq = FAQ.objects.all()
    return render(request, 'faq.html', {'faq': faq})


def politics(request):
    return render(request, 'politics.html')


def terms(request):
    return render(request, 'terms.html')


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
    send_mail(subject='Код подтверждения', message=message,
              from_email=EMAIL_HOST_USER, recipient_list=[email], fail_silently=True)
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
        data = json.loads(request.body)
        if not request.user.is_authenticated:
            email = data['email']
            passw = data['pass']
            user = authenticate(request=request, email=email,
                                password=passw)
            if user is None:
                return HttpResponse(status=400)
            login(request, user)
        type = data['type']
        number = data['number']
        if request.is_secure:
            protocol = 'https://'
        else:
            protocol = 'http://'
        host = request.META['HTTP_HOST']
        create_car_info_celery.delay(protocol, host, request.user.email, type, number)
        return HttpResponse(status=200)
    return HttpResponse(status=400)


def logout_(request):
    logout(request)
    return redirect(index)


def check_car(request):
    form = AuthForm()
    type = request.GET.get('type')
    if type == 'None':
        type = 'GOS'
    number = request.GET.get('number')
    context = {
        'form': form,
        'type': type,
        'number': number
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

    context = {
        'reports': reports
    }

    try:
        r = request.GET['redirect']
        context['redirect'] = True
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

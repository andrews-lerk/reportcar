import time
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
import json
from profiles.models import Profiles
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ObjectDoesNotExist
from reports.utils import create_car_info, get_restrict_car_info
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from reports.models import Vehicle, VinDecode, VehiclePeriods, Dtp, \
    Restrict, Wanted, Pledges, Reviews, Taxi, \
    CustomsClearance, RNISRegister, Osago, DiagnosticsActive, DiagnosticsExpired, Image


def index(request):
    if request.method == 'POST':
        form = AuthForm()
        type_ = request.POST.get('select')
        if type_ == None:
            type_ = 'GOS'
        try:
            number = request.POST['forminnumber']
        except:
            return HttpResponse(status=200)
        print(number)
        result = get_restrict_car_info(request, type_, number)
        context = {
            'type' : type_,
            'form': form,
            'number': number
        }
        try:
            context['model'] = result['model']
            context['color'] = result['color']
            context['year'] = result['year']
            context['car'] = True
        except:
            context['message'] = result['message']
            context['car'] = False
        return render(request, 'reports/restrict_report.html', context)
    return render(request, 'index.html')


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
    print(password)
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
    form = AuthForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(request=request, email=form.cleaned_data['email'],
                                password=form.cleaned_data['password'])
            print(user)
            login(request, user)
            return redirect('lk')
    return HttpResponse(status=400)


def auth_from_restrict(request):
    if not request.user.is_authenticated:
        form = AuthForm(request.POST)
    if request.method == 'POST':
        if request.user.is_authenticated:
            type = request.POST['type']
            number = request.POST['number']
            mesaages, errors, report = create_car_info(request, type, number)
            return redirect('report_detail', report.key)
        else:
            if form.is_valid():
                user = authenticate(request=request, email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'])
                login(request, user)
                type = request.POST['type']
                number = request.POST['number']
                mesaages, errors, report = create_car_info(request, type, number)
                return redirect('report_detail', report.key)
    return HttpResponse(status=400)


def logout_(request):
    logout(request)
    return redirect(index)


@login_required()
def lk(request):
    reports = Vehicle.objects.filter(profile=request.user)
    context = {
        'reports': reports
    }
    return render(request, 'lk.html', context)


def report_view(request):
    if request.method == 'POST':
        type = request.POST['selected']
        number = request.POST.get('formin')
        messages, errors = create_car_info(request, type, number)
        print(messages)
        print(errors)
        return redirect(index)

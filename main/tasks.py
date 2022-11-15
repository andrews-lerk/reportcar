from django.core.mail import send_mail

from config.celery import app
from config.settings import EMAIL_HOST_USER
from reports.utils import create_car_info
from .models import ReportsViewCounter


@app.task
def create_car_info_celery(protocol, host, email, type, number):
    create_car_info(protocol, host, email, type, number)


@app.task
def send_mail_(subject, text, email):
    send_mail(subject=subject, message=text,
              from_email=EMAIL_HOST_USER, recipient_list=[email], fail_silently=True)
    return 'Message done'


@app.task
def increment_counter():
    counter = ReportsViewCounter.objects.all().first()
    counter.value += 1
    counter.save()
    return 'Done'

from config.celery import app

from reports.utils import create_car_info
from .models import ReportsViewCounter
from celery import signals


@app.task
def create_car_info_celery(protocol, host, email, type, number):
    create_car_info(protocol, host, email, type, number)

@app.task
def increment_counter():
    counter = ReportsViewCounter.objects.all().first()
    counter.value+=1
    counter.save()
    return 'Done'
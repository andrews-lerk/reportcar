import os

from celery import Celery
from celery.schedules import crontab
from config.settings import BASE_DIR

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('pro_app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'increment-counter': {
        'task': 'main.tasks.increment_counter',
        'schedule': crontab(minute='*/5')
    }
}



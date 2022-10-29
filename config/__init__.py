from .celery import app as celery_app
from yookassa import Configuration

Configuration.account_id = '948023'
Configuration.secret_key = 'live_0zee8R4hHySUjfflHFpsmx0-ieZitUMSDSli4W_fWbg'

__all__ = ('celery_app',)
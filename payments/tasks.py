from config.celery import app
from .utils import subscribes_handler


@app.task
def subscribe_handler_():
    subscribes_handler()
    return 'handler done'

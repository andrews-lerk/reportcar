import datetime
from random import randint

import requests
from cryptography.fernet import Fernet
import base64

from django.utils import timezone
from .models import RecurrentOrder, Subscribe
from main.tasks import send_mail_
from config.settings import FERNET_SECRET_KEY as SECRET_KEY
from config.settings import CLOUDPAYMENTS_PUBLIC_ID, CLOUDPAYMENTS_API_PASSWORD


def random_invoice_id():
    return "".join([str(randint(0, 9)) for _ in range(15)])


def encrypt(data: str):
    return Fernet(SECRET_KEY.encode()).encrypt(data.encode()).decode()


def decrypt(data: str):
    return Fernet(SECRET_KEY.encode()).decrypt(data.encode()).decode()


def get_headers():
    key = base64.b64encode(f'{CLOUDPAYMENTS_PUBLIC_ID}:{CLOUDPAYMENTS_API_PASSWORD}'.encode('ascii')).decode()
    return {'Authorization': f'Basic {key}'}


def get_token_by_invoice_id(invoice_id):
    url = 'https://api.cloudpayments.ru/payments/list'
    body = {'date': timezone.now().date(), 'TimeZone': 'MSK'}
    response = requests.post(url=url, headers=get_headers(), data=body).json()
    result = []
    for i in response['Model']:
        if i['InvoiceId'] == invoice_id:
            result.append(i)
            break
    if not result:
        body = {'date': timezone.now().date() - timezone.timedelta(1), 'TimeZone': 'MSK'}
        response = requests.post(url=url, headers=get_headers(), data=body).json()
        for i in response['Model']:
            if i['InvoiceId'] == invoice_id:
                result.append(i)
                break
        if not result:
            return None
    return encrypt(result[0]['Token'])


def activate_subscribe(subscribe):
    url = 'https://api.cloudpayments.ru/payments/tokens/charge'
    invoice_id = random_invoice_id()
    body = {
        "Amount": subscribe.rate_type.base_price,
        "Currency": "RUB",
        "InvoiceId": invoice_id,
        "Description": f"Активация подписки {subscribe.rate_type.title} для пользователя {subscribe.profile.email}",
        "AccountId": subscribe.profile.email,
        "Email": subscribe.profile.email,
        "Token": decrypt(subscribe.payment_method.encrypted_token)
    }
    response = requests.post(url=url, headers=get_headers(), data=body).json()
    if response["Model"]["Status"] == "Completed":
        subscribe.process = "1"
        subscribe.status = "1"
        subscribe.process_date_expired = timezone.now() + datetime.timedelta(7)
        subscribe.reports_counter = subscribe.rate_type.reports_in_week
        subscribe.save()
        RecurrentOrder.objects.create(
            profile=subscribe.profile,
            subscribe=subscribe,
            invoice_id=invoice_id,
            payment_purpose=1,
            status=True
        )
        send_mail_.delay(subject='Успешная активация подписки',
                         text=f'Подписка {subscribe.rate_type.title} успешно активирована, вы можете '
                              f'в любой момент отменить подписку в личном кабинете по адресу https://reportcar.ru',
                         email=subscribe.profile.email)
    else:
        subscribe.process = "1"
        subscribe.status = "-1"
        subscribe.process_date_expired = timezone.now() + datetime.timedelta(7)
        subscribe.reports_counter = subscribe.rate_type.reports_in_week
        subscribe.save()
        RecurrentOrder.objects.create(
            profile=subscribe.profile,
            subscribe=subscribe,
            invoice_id=invoice_id,
            payment_purpose=1,
            status=False
        )
        send_mail_.delay(subject='Не удалось активировать подписку',
                         text=f'Подписка {subscribe.rate_type.title} не активирована из-за нехватки средств на '
                              f'счете, совершить повторную оплату можно '
                              f'в личном кабинете по адресу https://reportcar.ru, подписка будет автоматически '
                              f'отменена через 2 дня',
                         email=subscribe.profile.email)
    return


def regular_subscribe_pay(subscribe):
    url = 'https://api.cloudpayments.ru/payments/tokens/charge'
    invoice_id = random_invoice_id()
    body = {
        "Amount": subscribe.rate_type.base_price,
        "Currency": "RUB",
        "InvoiceId": invoice_id,
        "Description": f"Еженедельная оплата подписки {subscribe.rate_type.title} для пользователя {subscribe.profile.email}",
        "AccountId": subscribe.profile.email,
        "Email": subscribe.profile.email,
        "Token": decrypt(subscribe.payment_method.encrypted_token)
    }
    response = requests.post(url=url, headers=get_headers(), data=body).json()
    if response["Model"]["Status"] == "Completed":
        subscribe.process = str(int(subscribe.process) + 1)
        subscribe.status = "1"
        subscribe.process_date_expired = timezone.now() + datetime.timedelta(7)
        subscribe.reports_counter = subscribe.rate_type.reports_in_week
        subscribe.save()
        RecurrentOrder.objects.create(
            profile=subscribe.profile,
            subscribe=subscribe,
            invoice_id=invoice_id,
            payment_purpose=int(subscribe.process),
            status=True
        )
        send_mail_.delay(subject='Подписка успешно продлена',
                         text=f'Подписка {subscribe.rate_type.title} успешно продлена, '
                              f'Вам начислено {subscribe.rate_type.reports_in_week} отчетов. \n'
                              f'Управлять подпиской Вы можете '
                              f'в личном кабинете по адресу https://reportcar.ru',
                         email=subscribe.profile.email)
    else:
        subscribe.process = str(int(subscribe.process) + 1)
        subscribe.status = "-1"
        subscribe.process_date_expired = timezone.now() + datetime.timedelta(7)
        subscribe.reports_counter = subscribe.rate_type.reports_in_week
        subscribe.save()
        RecurrentOrder.objects.create(
            profile=subscribe.profile,
            subscribe=subscribe,
            invoice_id=invoice_id,
            payment_purpose=int(subscribe.process),
            status=False
        )
        send_mail_.delay(subject='Не удалось продлить подписку',
                         text=f'Подписка {subscribe.rate_type.title} не продлена из-за нехватки средств на '
                              f'счете. \nCовершить повторную оплату можно '
                              f'в личном кабинете по адресу https://reportcar.ru, подписка будет автоматически '
                              f'отменена через 2 дня',
                         email=subscribe.profile.email)
    return


def subscribe_continue_handler(subscribe):
    if subscribe.process_date_expired <= timezone.now():
        print(f'Subscribe for {subscribe.profile.email} do regular pay')
        regular_subscribe_pay(subscribe)
        return
    else:
        print(f'Subscribe for {subscribe.profile.email} do not need to do regular pay')
        return


def subscribe_finish_handler(subscribe):
    if subscribe.process_date_expired <= timezone.now():
        print(f'Subscribe for {subscribe.profile.email} finish')
        send_mail_.delay(subject='Подписка завершена',
                         text=f'Подписка {subscribe.rate_type.title} завершена! \n'
                              f'Оформить новую подписку можно по вдресу https://reportcar.ru/pricing',
                         email=subscribe.profile.email)
        subscribe.payment_method.delete()
        subscribe.delete()
        return
    else:
        print(f'Subscribe for {subscribe.profile.email} do not need finish')
        return


def subscribes_handler():
    queryset = Subscribe.objects.all()
    for subscribe in queryset:
        if subscribe.process == '0':
            if subscribe.process_date_expired <= timezone.now():
                activate_subscribe(subscribe)
                continue
            continue
        if subscribe.status == '1':
            process = int(subscribe.process)
            if process < 3:
                subscribe_continue_handler(subscribe)
            else:
                subscribe_finish_handler(subscribe)


import uuid

from yookassa import Payment


def get_payment(request, host, type, number):
    payment = Payment.create({
        "amount": {
            "value": "1.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"https://{host}/payments/pay-redirect"
        },
        "capture": True,
        "description": f"Оплата полного отчета для пользователя {request.user.email}",
        "metadata": {
            'type': type,
            'number': number,
            'user': request.user.email,
            'payment': 'one-time'
        }
    }, uuid.uuid4())
    return payment.json()


def get_subscribe_payment(request, host, rate):
    print('here')
    payment = Payment.create({
        "amount": {
            "value": f"{rate.start_price}.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"https://{host}/payments/pay-redirect"
        },
        "capture": True,
        "description": f"Оплата подписки на тариф '{rate.title}' для пользователя {request.user.email}",
        "metadata": {
            'typename': rate.title,
            'payment': 'subscribe'
        },
        "save_payment_method": True
    }, uuid.uuid4())
    return payment.json()

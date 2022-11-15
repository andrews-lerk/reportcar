from django.db import models
from profiles.models import Profiles


class Order(models.Model):
    profile = models.ForeignKey(Profiles, on_delete=models.CASCADE)
    invoice_id = models.CharField('ID заказа', max_length=31)
    status = models.BooleanField('Оплачено?', default=False)
    is_report_ready = models.BooleanField('Отчет составлен?', default=False)

    def __str__(self):
        return f'Платеж для  {self.profile.email}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class RecurrentOrder(models.Model):
    PAYMENT_PURPOSE = (
        (0, 'Оплата 3-х дневного периода'),
        (1, 'Оплата 1-ой недели'),
        (2, 'Оплата 2-ой недели'),
        (3, 'Оплата 3-ей недели'),
    )

    profile = models.ForeignKey(Profiles, on_delete=models.CASCADE)
    subscribe = models.ForeignKey('Subscribe', on_delete=models.SET_NULL, null=True)
    invoice_id = models.CharField('ID заказа', max_length=31)
    payment_purpose = models.CharField('Назначение платежа', choices=PAYMENT_PURPOSE, max_length=255)
    status = models.BooleanField('Оплачено?', default=False)

    def __str__(self):
        return f'Платеж подписки'

    class Meta:
        verbose_name = 'Платеж подписки'
        verbose_name_plural = 'Платежи подписок'


class PaymentMethod(models.Model):
    profile = models.ForeignKey(Profiles, on_delete=models.CASCADE)
    encrypted_token = models.TextField('Зашифрованный токен карты')

    def __str__(self):
        return f'Метод оплаты пользователя {self.profile.email}'

    class Meta:
        verbose_name = 'Метод оплаты'
        verbose_name_plural = 'Методы оплаты'


class Subscribe(models.Model):
    PROCESS = (
        ('0', '3 пробных дня'),
        ('1', '1-я неделя подписки'),
        ('2', '2-я неделя подписки'),
        ('3', '3-я неделя подписки'),
    )
    STATUS = (
        ('1', 'Активна'),
        ('-1', 'Приостановлена'),
    )

    profile = models.OneToOneField(Profiles, on_delete=models.CASCADE)
    rate_type = models.ForeignKey('RateType', on_delete=models.CASCADE)
    process = models.CharField('Текущий этап подписки', choices=PROCESS, max_length=255)
    process_date_expired = models.DateTimeField('Дата/время окончания текущего этапа подписки')
    status = models.CharField('Статус подписки', choices=STATUS, max_length=255)
    reports_counter = models.IntegerField()
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)

    def __str__(self):
        return f'Подписка пользователя {self.profile.email}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class RateType(models.Model):
    title = models.CharField('Название тарифа', max_length=255)
    start_price = models.IntegerField('Стартовая цена тарифа')
    base_price = models.IntegerField('Базовая цена тарифа в неделю')
    reports_in_week = models.IntegerField('Отчеты в неделю')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

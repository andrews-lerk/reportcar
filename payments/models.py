from django.db import models
from profiles.models import Profiles


class OneTimePayment(models.Model):
    profile = models.ForeignKey(Profiles, on_delete=models.CASCADE)

    payment_id = models.CharField('ID платежа', max_length=511)
    status = models.CharField('Статус платежа', max_length=31)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField('Оплачено?')

    class Meta:
        verbose_name = 'Разовый платеж'
        verbose_name_plural = 'Разовые платежи'

    def __str__(self):
        return f'Платеж для {self.profile}, ID - {self.payment_id}'


class SubscribePayment(models.Model):
    profile = models.ForeignKey(Profiles, on_delete=models.CASCADE)

    payment_id = models.CharField('ID платежа', max_length=511)
    status = models.CharField('Статус платежа', max_length=31)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField('Оплачено?')

    def __str__(self):
        return f'Автоплатеж для {self.profile}, ID - {self.payment_id}'

    class Meta:
        verbose_name = 'Платеж тарифа'
        verbose_name_plural = 'Платежи тарифов'


class SubscribePaymentMethod(models.Model):
    profile = models.OneToOneField(Profiles, on_delete=models.CASCADE)
    payment_method_id = models.CharField('ID сохраненного метода оплаты', max_length=511)
    saved = models.BooleanField()

    def __str__(self):
        return f'Способ оплаты для {self.profile}'

    class Meta:
        verbose_name = 'Сохраненный способ оплаты'
        verbose_name_plural = 'Сохраненные способы оплаты'


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


class RateSubscribe(models.Model):
    STEPS = (
        ('start', '3 пробных дня'),
        ('1week', '1-ая неделя тарифа из 3'),
        ('2week', '2-ая неделя тарифа из 3'),
        ('3week', '3-я неделя тарифа из 3'),
    )
    payment_method = models.OneToOneField(SubscribePaymentMethod, on_delete=models.CASCADE)
    rate_type = models.ForeignKey(RateType, on_delete=models.CASCADE)
    report_counter = models.IntegerField('Оставшеейся число отчетов')
    step = models.CharField('Текущий этап подписки', choices=STEPS, max_length=255)
    step_date_expired = models.DateField('Дата окончания текущего этапа подписки')

    def __str__(self):
        return f'Тариф для {self.payment_method.profile}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'



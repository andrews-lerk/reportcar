import random

from django.db import models
from django.urls import reverse

from profiles.models import Profiles


def random_value():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    result = ''
    for _ in range(31):
        result += random.choice(chars)
    return result


class Vehicle(models.Model):
    """ main model of vehicle, in this model connect all models of report via ForeignKey """

    profile = models.ForeignKey(Profiles, verbose_name='vehicle_profiles', on_delete=models.CASCADE)

    vin = models.CharField('Вин номер', max_length=511, null=True)
    gos_number = models.CharField('Регистрационный номер', max_length=255, null=True)
    body_number = models.CharField('Номер кузова', max_length=511, null=True)
    engine_number = models.CharField('Номер двигателя', max_length=511, null=True)
    model = models.CharField('Модель', max_length=511, null=True)
    color = models.CharField('Цвет', max_length=127, null=True)
    year = models.CharField('Год выпуска', max_length=16, null=True)
    engine_volume = models.CharField('Объем двигателя', max_length=127, null=True)
    power_hp = models.CharField('Мощность л.с', max_length=31, null=True)
    power_kwt = models.CharField('Мощность кВт.', max_length=31, null=True)
    category = models.CharField('Категория ТС', max_length=4, null=True)
    key = models.CharField('Уникальный ключ в базе данных', max_length=255, unique=True, default=random_value)

    def __str__(self):
        return f'{self.model} - {self.gos_number}'

    def get_absolute_url(self):
        return reverse('report_detail', kwargs={'key': self.key})


class Image(models.Model):
    vehicle = models.ForeignKey(Vehicle, verbose_name='vehicle_image', on_delete=models.CASCADE)

    img = models.URLField(null=True, blank=True)


class VinDecode(models.Model):
    """ VIN decoding vehicle data """

    vehicle = models.ForeignKey(Vehicle,verbose_name='vehicle_vindecode', on_delete=models.CASCADE)

    wmi = models.CharField('WMI', max_length=255, null=True)
    vis = models.CharField('VIS идентификатор', max_length=255, null=True)
    vds = models.CharField('VDS', max_length=255, null=True)
    year_identifier = models.CharField('Идентификатор года', max_length=255, null=True)
    serial_number = models.CharField('Серийный номер', max_length=255, null=True)
    vin_type = models.CharField('тип VIN', max_length=255, null=True)
    body_type = models.CharField('Тип кузова', max_length=255, null=True)
    engine_type = models.CharField('Тип двигателя', max_length=255, null=True)
    fuel_type = models.CharField('Тип топлива', max_length=255, null=True)
    transmission_type = models.CharField('Тип трансмиссии', max_length=255, null=True)
    car_class = models.CharField('Класс авто', max_length=255, null=True)
    car_type = models.CharField('Тип авто', max_length=255, null=True)
    body_diff = models.CharField('Отличие кузова', max_length=255, null=True)
    number_doors = models.CharField('Кол. дверей', max_length=255, null=True)
    number_seats = models.CharField('Кол. мест', max_length=255, null=True)
    engine_valves = models.CharField('Кол. клапанов двигателя', max_length=255, null=True)
    cylinders = models.CharField('Кол. цилиндров двигателя', max_length=255, null=True)
    transmission = models.CharField('Трансмиссия', max_length=255, null=True)


class VehiclePeriods(models.Model):
    """ Vehicle ownerships periods """

    vehicle = models.ForeignKey(Vehicle,verbose_name='vehicle_periods', on_delete=models.CASCADE)

    reason = models.CharField('Причина Регистрации', max_length=1023, null=True)
    owner = models.CharField('Владелец', max_length=127, null=True)
    date_from = models.CharField('Дата регистрации', max_length=31, null=True)
    to = models.CharField('Дата снятия с учета', max_length=31, null=True)
    period = models.CharField('Период владения', max_length=127, null=True)


class Wanted(models.Model):
    """ Vehicle wanted checks """

    vehicle = models.ForeignKey(Vehicle, verbose_name='vehicle_wanted', on_delete=models.CASCADE)

    region = models.CharField('Регион инициатора розыска', max_length=1023, null=True)
    model = models.CharField('Марка (модель) ТС', max_length=511, null=True)
    date = models.CharField('Дата постоянного учета в розыске', max_length=31, null=True)
    vin = models.CharField('VIN ТС', max_length=255, null=True)
    date_car = models.CharField('Год ТС', max_length=15, null=True)


class Restrict(models.Model):
    """ Vehicle restrict checks """

    vehicle = models.ForeignKey(Vehicle, verbose_name='vehicle_restrict', on_delete=models.CASCADE)

    region = models.CharField('Регион', max_length=255, null=True)
    basis_restrict = models.TextField('Основание ограничения', null=True)
    date_from = models.CharField('Дата наложения ограничения', max_length=31, null=True)
    date_to = models.CharField('Дата окончания ограничения', max_length=31, null=True)
    restrict = models.TextField('Вид ограничения', null=True)
    who_imposed = models.CharField('Кем наложено ограничение', max_length=511, null=True)


class Dtp(models.Model):
    """ Vehicle crashes checks """

    vehicle = models.ForeignKey(Vehicle, verbose_name='vehicle_dtp', on_delete=models.CASCADE)

    date = models.CharField('Дата ДТП', max_length=31, null=True)
    damage = models.CharField('Повреждения', max_length=1023, null=True)
    type = models.CharField('Тип ДТП', max_length=1023, null=True)
    damage_description = models.TextField('Описание инцидента', null=True)
    place = models.CharField('Место ДТП', max_length=255, null=True)


class DiagnosticsActive(models.Model):
    """ Vehicle active diagnostic card checks """

    vehicle = models.ForeignKey(Vehicle, verbose_name='vehicle_diagnostic_active', on_delete=models.CASCADE)

    from_date = models.CharField('Дата выдачи ДК', max_length=31, null=True)
    expire_date = models.CharField('Дата окончания ДК', max_length=31, null=True)
    value = models.CharField('Показания одометра', max_length=31, null=True)
    dc_number = models.CharField('Номер ДК', max_length=31, null=True)
    point_address = models.CharField('Адрес выдачи ДК', max_length=511, null=True)


class DiagnosticsExpired(models.Model):
    """ Vehicle expired diagnostic card checks """

    vehicle = models.ForeignKey(Vehicle, verbose_name='vehicle_diagnostic_expired', on_delete=models.CASCADE)

    from_date = models.CharField('Дата начала ДК', max_length=31, null=True)
    expire_date = models.CharField('Дата окончания ДК', max_length=31, null=True)
    value = models.CharField('Показания одометра', max_length=31, null=True)
    dc_number = models.CharField('Номер ДК', max_length=31, null=True)


class Osago(models.Model):
    """ Vehicle osago checks """

    vehicle = models.ForeignKey(Vehicle, verbose_name='vehicle_osago', on_delete=models.CASCADE)

    seria = models.CharField('Серия ОСАГО', max_length=255, null=True)
    number = models.CharField('Номер ОСАГО', max_length=255, null=True)
    organization = models.CharField('Наименование страховой организации', max_length=2047, null=True)
    status = models.CharField('Статус договора ОСАГО', max_length=255, null=True)

    term = models.CharField('Срок действия и период использования '
                            'транспортного средства договора ОСАГО', max_length=1023, null=True)

    region = models.CharField('Транспортное средство используется в регионе', max_length=1023, null=True)

    restrictions = models.CharField('Договор ОСАГО с ограничениями/без ограничений лиц, '
                                    'допущенных к управлению транспортным средством', max_length=2047, null=True)

    action = models.CharField('Транспортное средство следует к месту '
                              'регистрации или к месту проведения технического осмотра', max_length=511, null=True)

    usage_purposes = models.CharField('Цель использования транспортного средства', max_length=1023, null=True)
    insured = models.CharField('Страхователь', max_length=255, null=True)
    owner = models.CharField('Собственник', max_length=255, null=True)

    date_actual = models.CharField('Дата актуальности', max_length=31, null=True)


class Pledges(models.Model):
    """ Vehicle pledges checks """

    vehicle = models.ForeignKey(Vehicle, verbose_name='vehical_pledges', on_delete=models.CASCADE)

    record_date = models.CharField('Дата записи', max_length=1023, null=True)
    pledge_give = models.CharField('Залогодатель', max_length=1023, null=True)
    pledge_give_birthday = models.CharField('Дата рождения залогодателя', max_length=63, null=True)
    pledge_get = models.CharField('Залогодержатель', max_length=1023, null=True)


class Reviews(models.Model):
    """ Vehicle reviews checks """

    vehicle = models.ForeignKey(Vehicle, verbose_name='vehicle_reviews', on_delete=models.CASCADE)

    date = models.CharField('Дата отзыва', max_length=31, null=True)
    organization = models.CharField('Организатор', max_length=1023, null=True)
    reason = models.TextField('Причина отзыва', null=True)
    recommendation = models.TextField('Рекоммендации', null=True)


class Taxi(models.Model):
    """ Vehicle reviews checks """

    vehicle = models.ForeignKey(Vehicle, verbose_name='vehicle_taxi', on_delete=models.CASCADE)

    number = models.CharField('Номер разрешения', max_length=31, null=True)
    organization = models.CharField('Перевозчик, владелец лицензии', max_length=511, null=True)
    date_from = models.CharField('Дата выдачи разрешения', max_length=31, null=True)
    date_to = models.CharField('Дата окончания разрешения', max_length=31, null=True)
    status = models.CharField('Статус разрешения', max_length=31, null=True)
    region = models.CharField('Региональная принадлежность', max_length=255, null=True)


class CustomsClearance(models.Model):
    """ Info about customs clearance """

    vehicle = models.ForeignKey(Vehicle, verbose_name='vehicle_customs', on_delete=models.CASCADE)

    model = models.CharField('Модель', max_length=255, null=True)
    date = models.CharField('Дата выпуска в свободное обращение', max_length=255, null=True)


class RNISRegister(models.Model):
    """ Info about regist in RNIS """

    vehicle = models.ForeignKey(Vehicle, verbose_name='vehicle_rnis', on_delete=models.CASCADE)

    vehicle_exists = models.BooleanField('Зарегестрировано', default=False, null=True)
    last_mark = models.CharField('Дата/время передачи телематики', max_length=255, null=True)
    is_online = models.BooleanField('Телематика передается', default=False, null=True)

# Generated by Django 4.1.1 on 2022-10-28 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_ratesubscribe_report_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratetype',
            name='reports_in_week',
            field=models.IntegerField(default=1, verbose_name='Отчеты в неделю'),
            preserve_default=False,
        ),
    ]

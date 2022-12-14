# Generated by Django 4.1.1 on 2022-09-29 19:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_alter_image_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='date_actual',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата составления отчета'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicle',
            name='is_full_report',
            field=models.BooleanField(default=False, verbose_name='Полный отчет?'),
        ),
    ]

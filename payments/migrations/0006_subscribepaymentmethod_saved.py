# Generated by Django 4.1.1 on 2022-10-29 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_ratetype_reports_in_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribepaymentmethod',
            name='saved',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
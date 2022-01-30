# Generated by Django 3.2.3 on 2022-01-30 09:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20220130_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 9, 0, 32, 191738, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 30, 9, 0, 32, 191738, tzinfo=utc), editable=False),
        ),
    ]

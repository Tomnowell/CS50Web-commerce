# Generated by Django 3.2.4 on 2022-01-16 06:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20220116_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 23, 15, 23, 28, 529515)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 16, 15, 23, 28, 529515)),
        ),
    ]

# Generated by Django 3.2.4 on 2022-02-06 02:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 13, 2, 13, 9, 836090, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 2, 13, 9, 836090, tzinfo=utc), editable=False),
        ),
    ]
# Generated by Django 3.2.4 on 2022-01-16 06:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20220116_1520'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='owner',
            new_name='auctioneer',
        ),
        migrations.AlterField(
            model_name='listing',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 23, 15, 21, 57, 892928)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 16, 15, 21, 57, 892928)),
        ),
    ]

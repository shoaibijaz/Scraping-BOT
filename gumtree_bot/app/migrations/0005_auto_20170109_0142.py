# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170109_0017'),
    ]

    operations = [
        migrations.AddField(
            model_name='adslog',
            name='posted',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='adslog',
            name='published_in',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='searchlog',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 8, 20, 42, 56, 449114, tzinfo=utc)),
        ),
    ]

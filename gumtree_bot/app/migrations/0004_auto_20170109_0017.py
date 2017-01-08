# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20170108_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchlog',
            name='ads_count',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='searchlog',
            name='pages',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='searchlog',
            name='request_type',
            field=models.TextField(null=True, default='', blank=True),
        ),
    ]

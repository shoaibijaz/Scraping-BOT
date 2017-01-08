# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_adscomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchlog',
            name='proxy',
            field=models.TextField(default='', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='searchlog',
            name='source',
            field=models.TextField(default='manual', blank=True, null=True),
        ),
    ]

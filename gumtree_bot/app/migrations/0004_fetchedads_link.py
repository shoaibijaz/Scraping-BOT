# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 13:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_fetchedads_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='fetchedads',
            name='link',
            field=models.TextField(blank=True, null=True),
        ),
    ]
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdsComment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('text', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('ad', models.ForeignKey(to='app.AdsLog', related_name='Comments')),
            ],
            options={
                'db_table': 'app_ads_comment',
            },
        ),
    ]

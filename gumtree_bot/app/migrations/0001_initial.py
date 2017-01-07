# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdsLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('url', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'app_ads_logs',
            },
        ),
        migrations.CreateModel(
            name='SearchLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('url', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'app_search_logs',
            },
        ),
        migrations.AddField(
            model_name='adslog',
            name='search',
            field=models.ForeignKey(to='app.SearchLog', related_name='ads'),
        ),
    ]

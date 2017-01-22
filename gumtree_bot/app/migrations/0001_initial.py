# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdsComment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('text', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'app_ads_comment',
            },
        ),
        migrations.CreateModel(
            name='AdsLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('text', models.TextField()),
                ('url', models.TextField()),
                ('posted', models.TextField(blank=True, null=True)),
                ('published_in', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'app_ads_logs',
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('parent', models.ForeignKey(to='app.Categories', blank=True, null=True)),
            ],
            options={
                'db_table': 'app_categories',
            },
        ),
        migrations.CreateModel(
            name='SearchLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('text', models.TextField()),
                ('url', models.TextField()),
                ('source', models.TextField(blank=True, null=True, default='manual')),
                ('proxy', models.TextField(blank=True, null=True, default='')),
                ('pages', models.IntegerField(blank=True, default=0)),
                ('ads_count', models.IntegerField(blank=True, default=0)),
                ('request_type', models.TextField(blank=True, null=True, default='')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'app_search_logs',
            },
        ),
        migrations.CreateModel(
            name='Websites',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('function', models.TextField(blank=True, null=True)),
                ('search_url', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'app_websites',
            },
        ),
        migrations.AddField(
            model_name='adslog',
            name='search',
            field=models.ForeignKey(related_name='ads', to='app.SearchLog'),
        ),
        migrations.AddField(
            model_name='adscomment',
            name='ad',
            field=models.ForeignKey(related_name='Comments', to='app.AdsLog'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdsMessages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('message', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('phone', models.TextField(blank=True, null=True)),
                ('created_time', models.DateTimeField(blank=True)),
                ('modified_time', models.DateTimeField(blank=True)),
                ('status', models.IntegerField(default=3, choices=[(1, 'SENT'), (2, 'FAILED'), (3, 'PENDING')])),
            ],
            options={
                'db_table': 'ads_messages',
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('order', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(null=True, to='app.Categories', blank=True)),
            ],
            options={
                'db_table': 'app_categories',
            },
        ),
        migrations.CreateModel(
            name='FetchedAds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('ad_id', models.TextField(blank=True, null=True)),
                ('link', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('posted_on', models.TextField(blank=True, null=True)),
                ('price', models.TextField(blank=True, null=True)),
                ('image', models.TextField(blank=True, null=True)),
                ('category', models.TextField(blank=True, null=True)),
                ('location', models.TextField(blank=True, null=True)),
                ('page', models.IntegerField(blank=True, default=0, null=True)),
                ('created_time', models.DateTimeField(blank=True)),
                ('modified_time', models.DateTimeField(blank=True)),
                ('status', models.IntegerField(default=1, choices=[(1, 'VISIBLE'), (1, 'SOFT DELETE'), (3, 'INVALID')])),
            ],
            options={
                'db_table': 'app_fetched_ads',
            },
        ),
        migrations.CreateModel(
            name='Proxies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('IP', models.TextField(blank=True, null=True)),
                ('port', models.TextField(blank=True, null=True)),
                ('country', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'app_proxies',
            },
        ),
        migrations.CreateModel(
            name='SearchLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('keywords', models.TextField(blank=True, null=True)),
                ('negative', models.TextField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('type', models.TextField(blank=True, null=True)),
                ('total_pages', models.IntegerField(default=0)),
                ('total_ads', models.IntegerField(default=0)),
                ('category', models.ForeignKey(null=True, to='app.Categories', blank=True)),
                ('proxy', models.ForeignKey(null=True, to='app.Proxies', blank=True)),
            ],
            options={
                'db_table': 'app_search_log',
            },
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('start_time', models.DateTimeField(blank=True)),
                ('modified_time', models.DateTimeField(blank=True)),
                ('status', models.IntegerField(default=1, choices=[(1, 'Pending'), (2, 'Running'), (3, 'Stopped'), (4, 'Completed'), (5, 'Error')])),
                ('search', models.ForeignKey(related_name='search_tasks', to='app.SearchLog')),
            ],
            options={
                'db_table': 'app_tasks',
            },
        ),
        migrations.CreateModel(
            name='Websites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('function', models.TextField(blank=True, null=True)),
                ('search_url', models.TextField(blank=True, null=True)),
                ('country', models.TextField(blank=True, null=True)),
                ('comment_url', models.TextField(blank=True, null=True)),
                ('order', models.IntegerField(default=0, null=True)),
            ],
            options={
                'db_table': 'app_websites',
            },
        ),
        migrations.AddField(
            model_name='searchlog',
            name='website',
            field=models.ForeignKey(null=True, to='app.Websites', blank=True),
        ),
        migrations.AddField(
            model_name='fetchedads',
            name='task',
            field=models.ForeignKey(related_name='fetched_ads', to='app.Tasks'),
        ),
        migrations.AddField(
            model_name='categories',
            name='website',
            field=models.ForeignKey(null=True, to='app.Websites', blank=True),
        ),
        migrations.AddField(
            model_name='adsmessages',
            name='ad',
            field=models.ForeignKey(to='app.FetchedAds'),
        ),
    ]

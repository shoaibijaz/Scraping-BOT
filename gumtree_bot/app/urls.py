# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
    url(r'^$', DashboardView.as_view(), name='home'),
    url(r'^scraper/$', ScraperView.as_view(), name='scraper'),
    url(r'^scraper/(?P<id>\d+)/$', (ScraperView.as_view()), name='scraper'),
    url(r'^scraper_form/$', ScraperFormView.as_view(), name='scraper-form'),
    url(r'^extract_ads/$', ExtractAdsView.as_view(), name='extract-ads'),
    url(r'^stop_extract_ads/$', StopExtractAdsView.as_view(), name='stop-extract-ads'),
    url(r'^create_task/$', CreateTaskView.as_view(), name='create_task'),
    url(r'^get_ads_list/$', GetAdsListView.as_view(), name='ads-list'),
    url(r'^comment_form/$', CommentFormView.as_view(), name='comment-form'),
    url(r'^post_comment/$', PostCommentView.as_view(), name='post_comment'),
)

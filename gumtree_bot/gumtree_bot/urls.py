from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from app.views import *


urlpatterns = (
    url(r'^$', DashboardView.as_view(), name='home'),
    url(r'^http_get/$', HttpGet.as_view(), name='abc-a'),
    url(r'^extract_ads/$', ExtractAds.as_view(), name='extract'),
    url(r'^get_ads_list/$', GetAdsList.as_view(), name='ads)list'),
    url(r'^post_comment/$', PostCommentView.as_view(), name='post_comment'),
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from app.views import *


urlpatterns = patterns('',
                       url(r'^', include("app.urls")),
                       url(r'^api/', include("api.urls")),
                       url(r'^admin/', include(admin.site.urls)),

)

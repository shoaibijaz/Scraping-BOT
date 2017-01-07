from django.views.generic import TemplateView,View
from django.http import HttpResponse
from django.core import serializers

from app.bot import ScrapAds
from app.models import *
from app.bot_post import *

import json

class DashboardView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return self.render_to_response(context)


class HttpGet(View):

    def get(self, request, *args, **kwargs):
        content = ''

        url = request.GET.get('text', None)

        return HttpResponse(ScrapAds().search_status(url))


class ExtractAds(View):

    def get(self, request, *args, **kwargs):

        params = request.GET.get('params', None)

        ScrapAds().all_ads(params)

        return HttpResponse(1)


class GetAdsList(View):

    def get(self, request, *args, **kwargs):

        log_id = request.GET.get('log_id', None)

        ads = SearchLog.objects.get(pk=log_id).ads.all()

        return HttpResponse(serializers.serialize('json',ads))


class PostCommentView(View):

    def get(self, request, *args, **kwargs):

        ads = request.GET.get('ads', '')
        message = request.GET.get('message', '')

        return HttpResponse(WebDriver().post_comments(ads,message))
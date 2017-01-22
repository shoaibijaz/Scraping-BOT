from django.views.generic import TemplateView,View
from django.http import HttpResponse
from django.core import serializers

from app.bot import ScrapAds
from app.models import *
from app.bot_post import *
from app.forms import *

import json

class DashboardView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['form'] = SearchForm()

        return self.render_to_response(context)



    def post(self, request, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context['form'] = SearchForm(request.POST)

        print(context['form'])
        return HttpResponse(1)


class SearchAds(View):

    def get(self, request, *args, **kwargs):
        context = super(SearchAds, self).get_context_data(**kwargs)
        url = request.GET.get('text', None)
        response = ScrapAds().search_status(url)


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
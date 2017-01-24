from django.views.generic import TemplateView,View
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from app.bot import ScrapAds
from app.models import *
from app.bot_post import *
from app.forms import *
from app.Response import JSONResponse
from app.scrapers.scraper import Scraper

import json


class DashboardView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        return self.render_to_response(context)


class ScraperView(TemplateView):
    template_name = "scraper.html"

    def get(self, request, *args, **kwargs):
        context = super(ScraperView, self).get_context_data(**kwargs)

        id = kwargs.get('id', 0)

        return self.render_to_response(context)


class ScraperForm(TemplateView):
    template_name = "shared/scraper_form.html"

    def get(self, request, *args, **kwargs):
        context = super(ScraperForm, self).get_context_data(**kwargs)

        id = request.GET.get('id',0)

        search_log = SearchLog().get_safe_single(id)

        context['form'] = SearchForm( initial= {
            "id" : id,
            "keywords" : search_log.keywords,
            "category" : search_log.category,
            "negative" : search_log.negative,
            "start_time" : search_log.start_time,
            "end_time" : '',
            "ads" : search_log.total_ads,
            "pages" : search_log.total_pages,
            "website" : search_log.website,
            "proxy" : search_log.proxy

        })

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super(ScraperForm, self).get_context_data(**kwargs)

        try:

            form = SearchForm(request.POST)

            json_response = JSONResponse()

            if form.is_valid():
                data = form.cleaned_data
                json_response.status = JSONResponse.SUCCESS_STATUS
                json_response.data = Scraper.scrap_data(data)
            else:
                json_response = json_response.form_error_response(form)

            return HttpResponse(json_response.to_json())

        except Exception as ex:
            json_response = JSONResponse().exception_response(str(ex))
            return HttpResponse(json_response.to_json())


class SearchAds(TemplateView):

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
from django.views.generic import TemplateView, View, ListView
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


class ScraperFormView(TemplateView):
    template_name = "shared/scraper_form.html"

    def get(self, request, *args, **kwargs):
        context = super(ScraperFormView, self).get_context_data(**kwargs)

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
        context = super(ScraperFormView, self).get_context_data(**kwargs)

        try:

            form = SearchForm(request.POST)

            json_response = JSONResponse()

            if form.is_valid():
                data = form.cleaned_data
                json_response.status = JSONResponse.SUCCESS_STATUS
                json_response.data = Scraper.validate_data(data)
            else:
                json_response = json_response.form_error_response(form)

            return HttpResponse(json_response.to_json())

        except Exception as ex:
            json_response = JSONResponse().exception_response(str(ex))
            return HttpResponse(json_response.to_json())


class ExtractAdsView(View):

    def get(self, request, *args, **kwargs):

        try:
            log_id = request.GET.get('id', 0)
            task_id = request.GET.get('task', 0)

            json_response = JSONResponse()

            if log_id and int(log_id) > 0:
                json_response.data = Scraper.scrap_data(log_id, task_id)
                json_response.status = JSONResponse.SUCCESS_STATUS
            else:
                json_response = json_response.form_invalid_response('Please provide valid search ID.')

            return HttpResponse(json_response.to_json())

        except Exception as ex:
            json_response = JSONResponse().exception_response(str(ex))
            return HttpResponse(json_response.to_json())


class StopExtractAdsView(View):

    def get(self, request, *args, **kwargs):

        try:
            log_id = request.GET.get('id', 0)
            task_id = request.GET.get('task', 0)

            json_response = JSONResponse()

            if log_id and int(log_id) > 0 and task_id and int(task_id) > 0:
                task = Tasks.objects.get(pk=int(task_id))
                task.update_status(Tasks.STOPPED_STATUS)
                json_response.data = 1
                json_response.status = JSONResponse.SUCCESS_STATUS
            else:
                json_response = json_response.form_invalid_response('Please provide valid search ID.')

            return HttpResponse(json_response.to_json())

        except Exception as ex:
            json_response = JSONResponse().exception_response(str(ex))
            return HttpResponse(json_response.to_json())


class CreateTaskView(View):

    def get(self, request, *args, **kwargs):

        try:
            log_id = request.GET.get('id', 0)

            json_response = JSONResponse()

            if log_id and int(log_id) > 0:
                json_response.data = Tasks.save_item(log_id,Tasks.PENDING_STATUS).id
                json_response.status = JSONResponse.SUCCESS_STATUS
            else:
                json_response = json_response.form_invalid_response('Please provide valid search ID.')

            return HttpResponse(json_response.to_json())

        except Exception as ex:
            json_response = JSONResponse().exception_response(str(ex))
            return HttpResponse(json_response.to_json())


class GetAdsListView(ListView):
    template_name = 'shared/fetched_ads_list.html'
    context_object_name = 'items_list'

    def get_queryset(self):

        try:
            task_id = self.request.GET.get('id',0)

            return FetchedAds.objects.filter(task_id=int(task_id))

        except Exception as ex:
            raise ex


class CommentFormView(TemplateView):
    template_name = "shared/comment_form.html"

    def get(self, request, *args, **kwargs):
        context = super(CommentFormView, self).get_context_data(**kwargs)

        context['form'] = CommentForm()

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super(CommentFormView, self).get_context_data(**kwargs)


class PostCommentView(View):

    def get(self, request, *args, **kwargs):

        ads = request.GET.get('ads', '')
        message = request.GET.get('message', '')

        return HttpResponse(WebDriver().post_comments(ads,message))
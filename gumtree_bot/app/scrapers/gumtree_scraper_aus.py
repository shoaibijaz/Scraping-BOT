# -*- coding: utf-8 -*-

import requests
import json
import re
import time

from bs4 import BeautifulSoup
from app.models import *


class ScraperResponse:
    total_pages = 1
    log_id = None
    total_ads = 0

    def __init__(self):
        pass

    def __init__(self, pages, log, ads):
        self.total_pages = pages
        self.log_id = log
        self.total_ads = ads

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class GumtreeScraperAustralia:

    @classmethod
    def validate_search(cls, form_data):

        try:

            website = form_data['website']
            url = website.search_url.format(page=1, search=form_data['keywords'])
            r = requests.get(url)

            if r.status_code == 200:
                content = r.text

                if u"Sorry we didn't find any results for " not in content:

                    soup = BeautifulSoup(content, "html.parser")

                    total = soup.find('h1', {"class": 'breadcrumb__item'})

                    if total:
                        text = total.text.replace(',', '')
                        text = text[:text.index('ads')].strip()
                        numbers = re.findall(r'\d+', text)
                        total = numbers[len(numbers)-1] if len(numbers) > 0 else 0

                    if not total or total == '':
                        total = 0

                    pages = 1

                    last_page = soup.find('div', { "class":'pagerlinks' })

                    if last_page and len(last_page.find_all('a')) > 0:
                        btn_last_page = soup.find(True, {'class', 'paginator__button paginator__button-last'})

                        if btn_last_page:
                            numbers = re.findall(r'\d+', btn_last_page['href'])
                            pages = numbers[0] if len(numbers) > 0 else 1

                    search_log = SearchLog().save_item(formData=form_data,pages=pages,ads=total)

                    response = ScraperResponse(pages,search_log.id, total)

                    return response.to_json()

            return ScraperResponse(0,0,0).to_json()

        except Exception as ex:
            raise ex

    @classmethod
    def extract_ads(cls, search_log, task_id):
        try:

            result = 0

            website = search_log.website

            task_item = Tasks.objects.get(pk=int(task_id))
            task_item.update_status(Tasks.RUNNING_STATUS)

            print('Task({}) status updated to running.'.format(task_id))

            for page in range(1, search_log.total_pages + 1):

                print('Task({}) starting page {}.'.format(task_id, page))

                if not cls.check_task_status(task_item):
                    return Tasks.STOPPED_STATUS

                print('Task({}) waiting for {} .'.format(task_id, 3))

                time.sleep(3)

                print('Task({}) resumed after {} .'.format(task_id, 3))

                print('Task({}) status checking {} .'.format(task_id, task_item.status))

                url = website.search_url.format(page=page, search=search_log.keywords)

                print('Task({}) URL {} .'.format(task_id, url))

                cls.fetching_ads_info(task_item, url, page, website, search_log.negative)

            print('Task({}) completed..'.format(task_id))

            task_item.update_status(Tasks.COMPLETE_STATUS)
            return Tasks.COMPLETE_STATUS

        except Exception as ex:

            task_item.update_status(Tasks.ERROR_STATUS)
            print('Task({}) error {}..'.format(task_id, str(ex)))

            raise ex

    @classmethod
    def check_task_status(cls, task_item):
        try:

            task_item.refresh_from_db()

            print('Task({}) refreshed database and status {}.'.format(task_item.id, task_item.status))

            if task_item.status == Tasks.STOPPED_STATUS:
                print('Task({}) stopped .'.format(task_item.id))
                return False

            return True

        except Exception as ex:
            raise ex

    @classmethod
    def fetching_ads_info(cls, task_item, url, page, website, negative_words):

        try:

            if not cls.check_task_status(task_item):
                return Tasks.STOPPED_STATUS

            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")

            if r.status_code == 200:
                ads = soup.find_all(True, {"class": 'ad-listing__item'})

                fetched_ada_list = []

                for ad in ads:

                    if not cls.check_task_status(task_item):
                        return Tasks.STOPPED_STATUS

                    ad_id = ad['data-add-id'] if ad.has_attr('data-add-id') else ''

                    link = ad.find(True, {'class', 'ad-listing__title-link'})

                    name = link.text.strip() if link else ''

                    if type(negative_words) is str:
                        negative_words = negative_words.strip().split(',')

                    match = next((x.lower() for x in negative_words if x in name.lower()), False)

                    if not match:

                        url = link['href'] if link else ''

                        posted_date = ad.find(True, {"class", "ad-listing__date"})

                        posted_date = posted_date.text if posted_date else ''

                        category = ''

                        image = ad.find(True, {'class', 'ad-listing__thumb'})

                        image = image.find('img')['src'] if image and image.find('img') else ''

                        price = ad.find(True, {"class", "ad-listing__price"})

                        price = price.text if price else ''

                        location = ad.find(True, {'class', 'ad-listing__location'})

                        location = location.text if location else ''

                        fetched_ad = FetchedAds()

                        fetched_ad.ad_id = str(ad_id).strip()
                        fetched_ad.link = str(website.url + url).strip()
                        fetched_ad.name = str(name).strip()
                        fetched_ad.posted_on = str(posted_date).strip()
                        fetched_ad.price = str(price).strip()
                        fetched_ad.image = str(image).strip()
                        fetched_ad.category = str(category).strip()
                        fetched_ad.location = str(location).strip()
                        fetched_ad.page = page
                        fetched_ad.created_time = datetime.now()
                        fetched_ad.modified_time = datetime.now()
                        fetched_ad.task = task_item

                        fetched_ada_list.append(fetched_ad)

                FetchedAds.objects.bulk_create(fetched_ada_list)
                fetched_ada_list = []

            else:
                raise ValueError('URL {} returns status {}', url, r.status_code)

        except Exception as ex:
            print('Task({}) page {} failed {} .'.format(task_item.id, page, str(ex)))
            pass

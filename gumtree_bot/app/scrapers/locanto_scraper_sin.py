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


class Locanto:

    @classmethod
    def validate_search(cls, form_data):

        try:

            website = form_data['website']

            url = website.search_url.format(url=website.url, page='',
                                                search=form_data['keywords'].strip())

            if form_data['category']:
                url = website.search_url.format(url=form_data['category'].url, page='',
                                                search=form_data['keywords'].strip())
            url = url.replace('//?','?')

            print(url)
            r = requests.get(url)

            if r.status_code == 200:
                content = r.text

                if "Sorry, there are no matches for this search right now." not in content:

                    soup = BeautifulSoup(content, "html.parser")

                    total = soup.find(True, {"class": 'js-result_count'})

                    if total:
                        total = total.text.replace(',', '')

                    if not total or total == '':
                        total = 0

                    pages = 1

                    pages = soup.find('div', { "class":'paging' })

                    if pages:
                        target = pages.find_all("a")

                        if target and target[len(target)-2].text == '>>':
                            pages = 19
                        else:
                            pages = target[len(target)-2].text


                    search_log = SearchLog().save_item(formData=form_data,pages=pages,ads=total)

                    response = ScraperResponse(pages,search_log.id, total)

                    return response.to_json()

            return ScraperResponse(0,0,0).to_json()

        except Exception as ex:
            raise ex

    @classmethod
    def scrap_categories(cls):

            url = 'http://singapore.locanto.sg/'

            r = requests.get(url)

            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")

                website = Websites.objects.get(pk=6)

                cat_divs = soup.find_all(True, {'class','catlist'})

                for item in cat_divs:

                    parent = item.find(True,{'class','listtitle'})

                    if parent:
                        parent = parent.find("a")

                        category = Categories()
                        category.website = website
                        category.name = parent.text.strip()
                        category.url = parent['href'].strip()

                        category.save()

                        childs = item.find_all('li')

                        for child in childs:

                            child_category = Categories()
                            child_category.website = website
                            child_category.parent = category
                            child_category.name = child.find("a").text.strip()
                            child_category.url =  child.find("a")['href']

                            child_category.save()

    @classmethod
    def extract_ads(cls, search_log, task_id):
        try:

            result = 0

            website = search_log.website

            task_item = Tasks.objects.get(pk=int(task_id))

            task_item.update_status(Tasks.RUNNING_STATUS)

            print('Task({}) status updated to running.'.format(task_id))

            for page in range(0, search_log.total_pages):

                print('Task({}) starting page {}.'.format(task_id, page))

                if not cls.check_task_status(task_item):
                    return Tasks.STOPPED_STATUS

                print('Task({}) waiting for {} .'.format(task_id, 3))

                time.sleep(3)

                print('Task({}) resumed after {} .'.format(task_id, 3))

                print('Task({}) status checking {} .'.format(task_id, task_item.status))

                page_no = page if page > 0 else ''

                url = website.search_url.format(url=website.url, page=page_no,
                                                search=search_log.keywords.strip())

                if search_log.category:
                    url = website.search_url.format(url=search_log.category.url, page=page_no,
                                                search=search_log.keywords.strip())
                url = url.replace('//?','?')

                print('Task({}) URL {} .'.format(task_id, url))

                cls.fetching_ads_info(task_item, url, page, website)

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
    def fetching_ads_info(cls, task_item, url, page, website):

        try:

            if not cls.check_task_status(task_item):
                return Tasks.STOPPED_STATUS

            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")

            if r.status_code == 200 and (int(page) == 0 or 'page='+str(page) in r.url):

                ads = soup.find_all(True, {"class": 'resultRow'})

                fetched_ada_list = []

                for ad in ads:

                    if not cls.check_task_status(task_item):
                        return Tasks.STOPPED_STATUS

                    ad_id = ad.find('a').find(True,{'class', 'fav_box'})['data-for']

                    location = ad.find('a').find(True,{'class', 'textLoc'})

                    location = location.text if location else  ''

                    url = ad.find("a")['href']

                    name = ad.find('a').find(True,{'class', 'textHeader'}).text

                    posted_date = ''

                    category = ad.find(True,{'class', 'resultCat'})

                    category = category.text if category else ''

                    images = ad.find_all("img")

                    if images and len(images) > 0:
                        image = images[0]['data-src'] if images[0].has_attr('data-src') else ''
                        image =  images[0]['src'] if images[0].has_attr('src') else image

                    price = ad.find('strong')

                    price = price.text if price else ''

                    fetched_ad = FetchedAds()

                    fetched_ad.ad_id = str(ad_id).strip()
                    fetched_ad.location = location

                    fetched_ad.link = str(url).strip()
                    fetched_ad.name = str(name).strip()
                    fetched_ad.posted_on = str(posted_date).strip()
                    fetched_ad.price = str(price).strip()
                    fetched_ad.image = str(image).strip()
                    fetched_ad.category = str(category).strip()
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



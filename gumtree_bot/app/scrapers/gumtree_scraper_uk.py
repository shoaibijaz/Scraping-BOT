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


class GumtreeScraperUK:

    @classmethod
    def validate_search(cls, form_data):

        try:

            website = form_data['website']
            url = website.search_url.format(page=1, search=form_data['keywords'])
            r = requests.get(url)

            if r.status_code == 200:
                content = r.text

                if "Sorry we didn't find any results" not in content:

                    soup = BeautifulSoup(content, "html.parser")

                    total = soup.find('div', { "class":'srp-resultsheader' })

                    if total:
                        numbers = re.findall(r'\d+',  total.find("h1").text.replace(',', ''))
                        total = numbers[0]

                    if not total or total == '':
                        total = 0

                    pages = 1

                    last_page = soup.find('li', { "class":'pagination-next' })

                    if last_page:
                        text = re.findall(r'\d+',  last_page.text.replace(',', ''))
                        pages = int(text[1])

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

            if r.status_code == 200:
                ads = soup.find_all('a', {"class": 'listing-link'})

                fetched_ada_list = []

                for ad in ads:

                    if ad and ad['href'] and ad['href'] != '':

                        if not cls.check_task_status(task_item):
                            return Tasks.STOPPED_STATUS

                        link_split = re.findall(r'\d+', ad['href'])

                        ad_id = link_split[len(link_split)-1] if len(link_split) > 0 else ''

                        location = ad.find(True, {'class','listing-location'})
                        location = location.text if location else ''

                        url = website.url + ad['href']

                        posted_date = ad.find("div", {"class", "listing-posted-date"})

                        if posted_date and posted_date.find('span'):
                            posted_date = posted_date.find('span').text
                        else:
                            posted_date = ''

                        name = ad.find(True, {'class', 'listing-title'})

                        name = name.text if name else ''

                        image = ad.find("img")

                        if image and image.has_attr('src') and image['src']:
                            image = image['src']
                        elif image and image.has_attr('data-lazy') and image['data-lazy']:
                            image = image['data-lazy']
                        else:
                            image = ''

                        price = ad.find(True, {'class', 'listing-price'})
                        price = price.text if price else ''

                        attributes = ad.find(True, { 'class', 'listing-attributes' })

                        category = attributes.text if attributes else ''

                        fetched_ad = FetchedAds()

                        fetched_ad.ad_id = ad_id
                        fetched_ad.link = str(url).strip()
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

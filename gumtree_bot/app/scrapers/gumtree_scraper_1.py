import requests
import json
import re

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


class GumtreeScraperOne:

    @classmethod
    def validate_search(cls, form_data):

        try:

            website = form_data['website']
            url = website.search_url.format(page=1, search=form_data['keywords'])
            r = requests.get(url)

            if r.status_code == 200:
                content = r.text

                if 'Sorry, but we didn’t find any results. Below you can find some tips to help you in your search.' not in content:
                    soup =BeautifulSoup(content, "html.parser")

                    total = soup.find('span', { "class":'count' }).text.replace('ads','').replace(',','').strip()

                    pages = 1

                    last_page = soup.find('a', { "class":'last follows' })

                    if last_page:
                        href = last_page['href'].split('/')
                        pages = int(href[len(href)-1].replace('v1q0p', '').strip())

                    print(url)
                    search_log = SearchLog().save_item(formData=form_data,pages=pages,ads=total)

                    response = ScraperResponse(pages,search_log.id, total)

                    return response.to_json()

            return ScraperResponse(0,0,0)

        except Exception as ex:
            raise ex

    def all_ads(self, params):

        try:
            parsed = json.loads(params)

            text = parsed['q']
            pages = parsed['pages']

            search_log = SearchLog.objects.get(pk=parsed['log'])

            count = 0

            for num in range(1,pages+1):

                ads_logs = []

                url = self.make_url(text,num)
                r = requests.get(url)

                if r.status_code == 200:

                    soup = BeautifulSoup(r.text)

                    ads = soup.find_all('div', { "class":'container' })

                    for ad in ads:
                        link = ad.find("a",'href-link')
                        posted_date = ad.find("div",{"class","creation-date"}).find_all("span",'')[1].text
                        published_in = ad.find("div",{"class","category-location"}).find("span").text

                        ad_log = AdsLog(search=search_log,text=link.text,url=link['href'])
                        ad_log.posted = posted_date
                        ad_log.published_in = published_in

                        ads_logs.append(ad_log)
                        count += 1

                AdsLog.objects.bulk_create(ads_logs)

                slee

                if count >= 100:
                    return count

            return count

        except Exception as ex:
            print(ex)
            return 0

    @classmethod
    def make_url(cls, text, page):

        text = re.sub('\s+', ' ', text).strip().replace(' ','+')

        url = 'https://www.gumtree.sg/s-'+ text

        if page <= 1:
            url += "/v1q0p1"
        else:
            page = str(page)
            url += '/page-'+ page + "/v1q0p" + page

        return url
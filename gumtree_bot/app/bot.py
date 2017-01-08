import requests
import json
import re

from bs4 import BeautifulSoup
from app.models import *

class ScrapAds():

    def search_status(self, text):

        total, pages, db = 0, 0 ,0

        try:
            if SearchLog.count_keyword(text) > 0:
                search_log = SearchLog.first_by_keyword(text)
                total = search_log.ads_count
                pages = search_log.pages
                db = 1
                log_id = search_log.id

                return { 'total':total, 'pages':pages, "log":log_id, "q":text, "db":db }

            url = self.make_url(text,1)
            r = requests.get(url)

            search_log = SearchLog(text=text,url=url, source='manual',request_type='requests')
            search_log.save()

            if r.status_code==200:
                content = r.text

                if 'Sorry, but we didn’t find any results. Below you can find some tips to help you in your search.' not in content:
                    soup = BeautifulSoup(content)

                    total = soup.find('span', { "class":'count' }).text.replace('ads','').replace(',','').strip()

                    pages = 1

                    last_page = soup.find('a', { "class":'last follows' })

                    if last_page:
                        href = last_page['href'].split('/')
                        pages = int(href[len(href)-1].replace('v1q0p','').strip())

            search_log.ads_count = total
            search_log.pages = pages
            search_log.save()

            return { 'total':total, 'pages':pages, "log":search_log.id, "q":text, "db":db }

        except Exception as ex:
            print(ex)
            return { 'total':0, 'pages':0, "log":-1, "q":text, "db":0 }

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

        text =re.sub( '\s+', ' ', text ).strip().replace(' ','+')

        url = 'https://www.gumtree.sg/s-'+ text

        if page <= 1:
            url += "/v1q0p1"
        else:
            page = str(page)
            url += '/page-'+ page + "/v1q0p" + page

        return  url
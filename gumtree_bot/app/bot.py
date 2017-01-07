import requests
import json
import re

from bs4 import BeautifulSoup
from app.models import *

class ScrapAds():

    def search_status(self, text):

        total,pages= 0,0

        url = self.make_url(text,1)
        r = requests.get(url)

        search_log = SearchLog(text=text,url=url)
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

        response = {'total':total, 'pages':pages, "log":search_log.id, "q":text}

        return json.dumps(response)

    def all_ads(self, params):

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
                ads = soup.find_all('a', { "class":'href-link' })

                for ad in ads:
                    ad_log = AdsLog(search=search_log,text=ad.text,url=ad['href'])
                    ads_logs.append(ad_log)
                    count += 1

            AdsLog.objects.bulk_create(ads_logs)

            if count >= 100:
                return count

        return count

    @classmethod
    def make_url(self, text, page):

        text =re.sub( '\s+', ' ', text ).strip().replace(' ','+')

        url = 'https://www.gumtree.sg/s-'+ text

        if page <= 1:
            url += "/v1q0p1"
        else:
            page = str(page)
            url += '/page-'+ page + "/v1q0p" + page

        return  url
import requests
import json
import time

from app.models import *


class CommentBot:

    @classmethod
    def post_comment(cls, form_data):

        try:

            ads_list = str(form_data['ads']).split(',')

            count = 0

            for ad_id in ads_list:
                ad = FetchedAds.objects.get(pk=int(ad_id))
                website = ad.task.search.website

                if website:
                    if cls.post_to_sin(form_data,ad,website):
                        count += 1

                time.sleep(5)

            return count

        except Exception as ex:
            raise ex

    @classmethod
    def post_to_sin(cls, form_data, ad, website):

        try:

            headers = {}

            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
            headers['Content-Type'] = 'application/json; charset=UTF-8'

            data = {
                'msgID':'1105651255',
                'action':'new_conversation',
                'email_message':'Price',
                'email':'endrew@yahoo.com'
            }

            data = json.dumps(data)

            session = requests.Session()

            response = session.post(website.comment_url, headers=headers, data=data)

            print(response.text)

            if response and response.status_code == 200 and '"replyFieldValid":true' in response.text:
                AdsMessages.save_item(form_data,ad,AdsMessages.SENT_STATUS)
                return True
            else:
                AdsMessages.save_item(form_data,ad, AdsMessages.FAILED_STATUS)
                return False

            return False

        except Exception as ex:
            return False

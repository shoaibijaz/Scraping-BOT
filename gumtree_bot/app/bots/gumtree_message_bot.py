from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import requests
import json
import time

from app.models import *


class CommentBot:

    @classmethod
    def post_comment(cls, form_data):

        try:

            task = Tasks.objects.get(pk=int(form_data['task']))

            task.update_status(Tasks.RUNNING_STATUS)

            ads_list = str(form_data['ads']).split(',')

            count = 0

            for ad_id in ads_list:

                if not cls.check_task_status(task):
                    return count

                ad = FetchedAds.objects.get(pk=int(ad_id))

                website = ad.task.search.website

                if website and website.function == 'gumtree_1':
                    if cls.post_to_sin(form_data,ad,website):
                        count += 1
                elif website and website.function == 'gumtree_3':
                        if cls.post_to_aus(form_data,ad,website):
                            count += 1

                time.sleep(5)

            task.update_status(Tasks.COMPLETE_STATUS)

            return count

        except Exception as ex:
            raise ex

    @classmethod
    def post_to_sin(cls, form_data, ad, website):

        try:

            headers = {}

            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
            headers['Content-Type'] = 'application/json; charset=UTF-8'

            message = "I'm interested.  Please contact me.↵When and where can I see it?↵↵";

            phone = form_data['phone']

            data = {
                'machineId': "",
                'adId':ad.ad_id,
                'buyerName':form_data['name'],
                'email':form_data['email'],
                'fileName':'',
                'phoneNumber':phone,
                'rand':'',
                'replyMessage':message + form_data['message']
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

    @classmethod
    def post_to_uk(cls, form_data, ad, website):

        try:

            headers = {}

            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
            headers['Content-Type'] = 'application/json; charset=UTF-8'

            message = "I'm interested.  Please contact me.↵When and where can I see it?↵↵";

            phone = form_data['phone']

            data = {
                'form.message': "",
                'form.senderName':ad.ad_id,
                'form.senderEmail':form_data['name'],
                'form.advertId':form_data['email'],
                'form.advertClickSource':'other',
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

    @classmethod
    def post_to_aus(cls, form_data, ad, website):

        driver = None
        sent_status, sent = AdsMessages.FAILED_STATUS, False

        try:

            url = ad.link
            driver = webdriver.Firefox()

            try:
                driver.set_page_load_timeout(5000)
                driver.get(url)

                element_present = EC.presence_of_element_located((By.ID, 'reply-form-send-message'))
                WebDriverWait(driver, 5).until(element_present)

            except TimeoutException:
                print ("Timed out waiting for page to load")

            if len(driver.find_elements_by_id('reply-form-send-message')) > 0:
                driver.find_element(By.ID,'reply-form-send-message').click()

                time.sleep(3)

                if len(driver.find_elements_by_id('viewad-contact-submit')) > 0:

                    driver.find_element(By.ID, 'message').send_keys(form_data['message'])
                    driver.find_element(By.ID, 'viewad-contact-name').send_keys(form_data['name'])
                    driver.find_element(By.ID,'from').send_keys(form_data['email'])

                    if len(driver.find_elements_by_id('reply-form-copy')) > 0:
                        driver.find_element(By.ID,'reply-form-copy').click()

                    driver.find_element(By.ID,'viewad-contact-submit').click()
                    sent = True
                    sent_status = AdsMessages.SENT_STATUS

                    time.sleep(1)

            AdsMessages.save_item(form_data,ad,sent_status)

            cls.quit_selenium(driver)

            time.sleep(2)

            return sent

        except Exception as ex:
            print(ex)
            cls.quit_selenium(driver)
            return False

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
    def quit_selenium(cls,driver):
        try:
            driver.quit()
            driver.close()
        except Exception as ex:
            print('Quit Selenium')
            pass
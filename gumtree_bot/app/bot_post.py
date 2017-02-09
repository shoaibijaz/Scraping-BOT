from .models import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

import logging

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

log = logging.getLogger(__name__)
log.addHandler(NullHandler())

from pyvirtualdisplay import Display
from selenium import webdriver

class WebDriver():

    @classmethod
    def sel_post(cls, url):

        log_path = '/var/log/apache2/geckodriver.log'

        driver = webdriver.Firefox(log_path = log_path)

        try:

            display = Display(visible=0, size=(800, 600))
            display.start()

            driver.get(url)

            time.sleep(5)

            chk_elem = driver.find_element_by_xpath("//ul[@class='canned-responses']/li[2]/label/input")
            chk_elem.click()

            text_ele = driver.find_element_by_name('replyMessage')

            text_ele.send_keys('I want to get!')

            text_name = driver.find_element_by_name('buyerName')

            text_name.send_keys('Dev')

            text_mail = driver.find_element_by_name('email')

            text_mail.send_keys('dev.gumtree001@gmail.com')

            text_phone = driver.find_element_by_name('phoneNumber')

            text_phone.send_keys('91180187')

            btn = driver.find_element_by_xpath("//button[@class='submit-reply']")
            btn.click()

            time.sleep(2)

            cls.quit_it(driver)

            display.stop()

            return True

        except TimeoutException as ex:
            log.debug('Error: at post_to_sin ' + str(ex))
            print ("Loading took too much time!")
            return False


    @classmethod
    def quit_it(cls,driver):
        try:
            driver.quit()
            driver.close()
            return;
        except Exception as ex:
            return
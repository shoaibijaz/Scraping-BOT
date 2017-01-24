from .models import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class WebDriver():

    def post_comments(self,ads,message):

        adsObject = SearchLog()

        count = 0
        for item in adsObject:
            ad_comment= SearchLog()
            ad_comment.ad = item
            ad_comment.text = message

            if self.sel_post(message,item.url):
                ad_comment.save()
                count +=1

        return count

    @classmethod
    def sel_post(cls,message,url):

        url  = 'https://www.gumtree.sg' +url

        driver = webdriver.Firefox()

        delay = 10

        driver.get("https://www.gumtree.sg/login.html")

        try:

            time.sleep(5)

            #WebDriverWait(driver, delay).until(EC.presence_of_element_located(driver.find_element_by_id('login-button')))
            #print ("Page is ready!")

            emailInput = driver.find_element_by_name("email")
            emailInput.send_keys("dev.gumtree001@gmail.com")

            passwordInput = driver.find_element_by_name("password")
            passwordInput.send_keys("dev.gumtree001@123")

            button = driver.find_element_by_id("login-button")
            button.click()

            time.sleep(5)

            #WebDriverWait(driver, delay).until(EC.presence_of_element_located(driver.find_element_by_class_name('button')))

            driver.get(url)

            time.sleep(5)

            #WebDriverWait(driver, delay).until(EC.presence_of_element_located(driver.find_element_by_class_name('button')))

            chk_elem = driver.find_element_by_xpath("//ul[@class='canned-responses']/li[2]/label/input")
            chk_elem.click()

            text_ele = driver.find_element_by_name('replyMessage')
            text_ele.send_keys(message)

            btn = driver.find_element_by_xpath("//button[@class='submit-reply']")
            btn.click()

            time.sleep(5)

            cls.quit_it(driver)

            return True

        except TimeoutException as ex:
            print ("Loading took too much time!")
            return False

        driver.close()

    @classmethod
    def quit_it(cls,driver):
        try:
            driver.quit()
            driver.close()
            return;
        except Exception as ex:
            return
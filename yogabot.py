import os

from selenium import webdriver
import time
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from apscheduler.schedulers.blocking import BlockingScheduler
'''
set 2 env vars YS_EMAIL and YS_PASSWORD with your email and password to log in to yogast8.com
also need to substitute relevant values in lines 14-25 
'''

#find mbo_id by inspecting the page near the class description as this link is not yet  visible (5 digit number) - screenshot attached
#there seems to be a pattern, e.g. strong this sun is 13099 and strong next sunday is 13100
mbo_id = "13100"
weekday = "Sun." # abbreviation with period - e.g. Thurs.
month = "Feb"
day = "6"
year = "2021"
hour = "10"
minute = "30" #or 00
ampm = "am"
classname = "STRONG"
PATH = "/Applications/chromedriver" #substitute path to your Selenium driver for Chrome

run_time = datetime(2021,1,31,0,0,1) #sub in the time you want it to run

registration_url = f"https://cart.mindbodyonline.com/sites/93972/cart/add_booking?item%5Binfo%5D={weekday}+{month}+{day}%2C+{year}+{hour}%3A{minute}{ampm}" +               \
                   f"&amp;item%5Bmbo_id%5D={mbo_id}&amp;item%5Bmbo_location_id%5D=1&amp;item%5Bname%5D={classname}&amp;item%5Btype%5D=Class"


# format https://cart.mindbodyonline.com/sites/93972/cart/add_booking?item%5Binfo%5D=Tue.+Feb++2%2C+2021++4%3A30+pm&item%5Bmbo_id%5D=13920&item%5Bmbo_location_id%5D=1&item%5Bname%5D=STRONG&item%5Btype%5D=Class&source=schedule_v1
def book_st8_next_week(url: str):
    driver = webdriver.Chrome(PATH)
    success = False
    driver.get(url)
    next = driver.find_element_by_class_name("cart-cta-preview-confirmation")
    next.click()
    time.sleep(10)
    name = driver.find_element_by_id("mb_client_session_username")
    name.send_keys(os.environ['YS_EMAIL'])
    name = driver.find_element_by_id("mb_client_session_password")
    name.send_keys(os.environ['YS_PASSWORD'])
    name.send_keys(Keys.RETURN)

    error = driver.find_element_by_class_name("c-banner--error")

    time.sleep(5)
    driver.quit()
    if not error:
        print("success")
        return True
    else:
        print("fail")
        return False



s = BlockingScheduler()
s.add_job(book_st8_next_week,'date', run_date=run_time)
s.start()
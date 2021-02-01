import os

from PIL.Image import Image
from selenium import webdriver
import time
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from apscheduler.schedulers.blocking import BlockingScheduler

'''
set 2 env vars YS_EMAIL and YS_PASSWORD with your email and password to log in to yogast8.com
also need to substitute relevant values in lines 18-24 
'''

PATH = "C:\\Users\\kmarx-levi\\Downloads\\chromedriver_win32\\chromedriver.exe" #substitute path to your Selenium driver for Chrome
#find mbo_id by inspecting the page near the class description as this link is not yet  visible (5 digit number) - screenshot attached
#there seems to be a pattern, e.g. strong this sun is 13099 and strong next sunday is 13100
mbo_id = "13100"
classname = "STRONG" # if multiple words separate with "+", e.g. "ST8+2+STILL"


class_datetime = datetime(year=2021, month=2, day=13, hour=10, minute=30)

script_run_datetime = datetime(year=2021, month=2, day=6, hour=0, minute=0, second=1) #sub in the time you want it to run
'''

mbo_id = "12792"
classname ="ST8+2+STILL"

class_datetime = datetime(year=2021, month=2, day=8, hour=16, minute=30)

script_run_datetime = datetime(year=2021, month=2, day=1, hour=8, minute=15, second=0)
'''

def save_screenshot(self, driver, file_name_prefix):
    img_str64 = driver.get_screenshot_as_base64()
    f = open("screenshots/%s.png" % file_name_prefix, "wb")
    f.write(img_str64.decode("base64"))
    f.close()

# format https://cart.mindbodyonline.com/sites/93972/cart/add_booking?item%5Binfo%5D=Tue.+Feb++2%2C+2021++4%3A30+pm&item%5Bmbo_id%5D=13920&item%5Bmbo_location_id%5D=1&item%5Bname%5D=STRONG&item%5Btype%5D=Class&source=schedule_v1
def book_st8_next_week(dt: datetime, mbo_id: str, classname: str):

    weekday = class_datetime.strftime("%a") + "." # abbreviation with period - e.g. Thurs.
    month =  class_datetime.strftime("%b") # Feb
    day =  class_datetime.strftime("%e")
    # e.g. 6
    year = class_datetime.strftime("%Y") # e.g."2021"
    hour = class_datetime.strftime("%I") # e.g. 10
    minute = class_datetime.strftime("%M") # e.g.  00
    ampm = class_datetime.strftime("%p").lower() # e.g. am

    registration_url = f"https://cart.mindbodyonline.com/sites/93972/cart/add_booking?item%5Binfo%5D={weekday}+{month}+{day}%2C+{year}+{hour}%3A{minute}{ampm}" + \
                       f"&amp;item%5Bmbo_id%5D={mbo_id}&amp;item%5Bmbo_location_id%5D=1&amp;item%5Bname%5D={classname}&amp;item%5Btype%5D=Class"


    driver = webdriver.Chrome(PATH)
    driver.get(registration_url)
    next = driver.find_element_by_class_name("cart-cta-preview-confirmation")
    next.click()
    time.sleep(10)
    name = driver.find_element_by_id("mb_client_session_username")
    name.send_keys(os.environ['YS_EMAIL'])
    name = driver.find_element_by_id("mb_client_session_password")
    name.send_keys(os.environ['YS_PASSWORD'])
    name.send_keys(Keys.RETURN)
    # driver.get_screenshot_as_file(f"/result/{classname}_{class_datetime}.png")


    try:
        error = driver.find_element_by_class_name("c-banner--error")
        print(f"failure! text = [{error.text}]")
        time.sleep(5)
        driver.quit()
        return False
    except NoSuchElementException:
        print("success")
        time.sleep(5)
        driver.quit()
        return True




s = BlockingScheduler()
s.add_job(lambda: book_st8_next_week(class_datetime, mbo_id, classname), 'date', run_date=script_run_datetime)
s.start()
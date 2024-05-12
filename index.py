from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
import pywhatkit as pwt
import requests
import shutil
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import schedule
import os
import glob
# from icecream import ic


class Aurora_Tracker():
    def __init__(self) -> None:
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # chrome_options.add_experimental_option('prefs',{'profile.default_content_setting_values.notifications':2})
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1920,1080)
    
    def __save_image(self, url):
        response = requests.get(url, stream=True)

        imgPath = "V:\\Personal Projects\\Automations\\NOAA_AuroraTracker\\images\\aurora_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        with open(imgPath, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        return imgPath

    def check_aurora(self, url):
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="product-grid-1"]/tbody/tr/td[1]/a/img')))
        viewlineImages = self.driver.find_element(By.XPATH, '//*[@id="product-grid-1"]/tbody/tr/td[1]/a/img')
        print(viewlineImages.get_attribute("src"))
        savedImg = self.__save_image(viewlineImages.get_attribute("src"))
        self.send_whatsapp_msg(savedImg)   
        # sleep(3600) 
        

    def send_whatsapp_msg(self, msg):
        currTime = datetime.now()
        if currTime.minute < 58:
            # pwt.sendwhatmsg("+16092332746", msg, currTime.hour, currTime.minute + 1)
            pwt.sendwhats_image("+16092332746", msg, "Aurora_Update_"+str(currTime), currTime.hour, currTime.minute + 1)
        else:
            # pwt.sendwhatmsg("+16092332746", msg, currTime.hour + 1, 0)
            pwt.sendwhats_image("+16092332746", msg, "Aurora_Update_"+str(currTime), currTime.hour + 1, 0)


tracker = Aurora_Tracker()
schedule.every(5).minutes.do(tracker.check_aurora, 'https://www.swpc.noaa.gov/products/aurora-viewline-tonight-and-tomorrow-night-experimental')

while True:
    schedule.run_pending()
    sleep(1)

# files = glob.glob('V:\\Personal Projects\\Automations\\NOAA_AuroraTracker\\images\\*')
# for f in files:
#     os.remove(f)
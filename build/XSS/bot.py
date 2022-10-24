from threading import Thread
import time
from os import getenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

USERNAME = getenv('USERNAME')
PASSWORD = getenv('PASSWORD')

class Bot(Thread):
    def __init__(self, uuid):
        Thread.__init__(self)
        self.uuid = uuid

    def run(self):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(service=Service('./geckodriver'), options=options)
        driver.get(f'http://localhost:5000/render/{self.uuid}')
        try:
            username = driver.find_element(By.ID, 'username')
            assert username.tag_name == 'input'
            password = driver.find_element(By.ID, 'password')
            assert password.tag_name == 'input'
        except:
            pass
        else:
            username.send_keys(USERNAME)
            username.send_keys(Keys.ENTER)
            password.send_keys(PASSWORD)
            password.send_keys(Keys.ENTER)
        finally:
            time.sleep(10)
            driver.quit()

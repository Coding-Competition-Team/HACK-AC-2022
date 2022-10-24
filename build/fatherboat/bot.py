import logging
from os import getenv
import re
from threading import Thread
import time

import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

pin = getenv("WERKZEUG_DEBUG_PIN")

class Bot(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.url = url

    def run(self):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(service=Service('./geckodriver'), options=options)

        # unimportant backend initlization pls ignore
        console = requests.get('http://localhost:5000/console').content.decode()
        secret = re.search('SECRET = "(.*)"', console).group(1)
        driver.get(f'localhost:5000/console?__debugger__=yes&cmd=pinauth&pin={pin}&s={secret}')

        # +----------------------+
        # | Visits your URL!!!!! |
        # +----------------------+

        driver.get(self.url)
        time.sleep(100)
        driver.quit()

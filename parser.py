import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

URL = 'https://ru.investing.com/currencies/usd-rub'

'''
def connect(url=URL):
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    driver.get(URL)
    element = driver.find_element("xpath", "/html/body/div[1]/div[2]/div/div/div[2]/main/div/div[1]/div[2]/div[1]/span")
    while True:
        print(BeautifulSoup(element.text, "html.parser"))
        return BeautifulSoup(element.text, "html.parser")
        time.sleep(2)
'''
global driver, element


def start_browser(url=URL):
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    driver.get(URL)
    element = driver.find_element("xpath", "/html/body/div[1]/div[2]/div/div/div[2]/main/div/div[1]/div[2]/div[1]/span")
    print('Browser Started')


def get_course():
    return BeautifulSoup(element.text, "html.parser")

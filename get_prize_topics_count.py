# //*[@id="site-content"]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div[2]/span[1]
import re
import time
from telnetlib import EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    driver.get("https://www.kaggle.com/c/m5-forecasting-accuracy/discussion")


    return driver


LINK_PRIZE_SIZE = '''//*[@id="site-content"]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div[2]'''
LINK_ORGANIZATOR_NAME = '''//*[@id="site-content"]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[3]/div/ul/li[1]/span/span[2]'''
LINK_TOPIC = '''//*[@id="site-content"]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/span[0]/text()'''
# the linc Topic doeasn't give the correct result

def get_prize_size(driver):
    """
   extract prize size from competition page
   :param driver: chrome driver
   :return: int prize size
   """
    try:
        prize = driver.find_element_by_xpath(LINK_PRIZE_SIZE).text
        prize_size = int(re.sub('\D', '', prize))
        print('prize: OK', prize_size)
    except:
        print('prize size: not now')
        prize_size = 0
    return prize_size


def organizator_name(driver):
    """
   extract organizator name from competition page
   :param driver: chrome driver
   :return: str organizator name
   """
    try:
        organizator = driver.find_element_by_xpath(LINK_ORGANIZATOR_NAME).text
        print('organizator: OK', organizator)
    except:
        print('organizator: not now')
        organizator = 'no name'
    return organizator


def get_number_of_topics(driver):
    """
    extract  number of topics from competition/ page
    :param driver: chrome driver
    :return: int number of topics
    """
    try:
        num_of_topics = driver.find_element_by_xpath(LINK_TOPIC).text
    except:
        print('topics: not now')
        num_of_topics = 'NOTHING THERE'
    return (num_of_topics)


if __name__ == '__main__':
    # get_prize_size(create_driver())

    # organizator_name(create_driver())

    get_number_of_topics(create_driver())
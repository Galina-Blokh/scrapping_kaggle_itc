import logging
import re
from selenium import webdriver

logging.basicConfig(filename='main.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    driver.get("https://www.kaggle.com/c/m5-forecasting-accuracy/discussion")

    return driver


LINK_PRIZE_SIZE = '''//*[@id="site-content"]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div[2]'''
LINK_ORGANIZATOR_NAME = '''//*[@id="site-content"]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[3]/div/ul/li[1]/span/span[2]'''

LINK_TOPIC = '''//*[@id="site-content"]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/span'''


def get_prize_size(driver):
    """
   extract prize size from competition page
   :param driver: chrome driver
   :return: int prize size
   """
    try:
        prize = driver.find_element_by_xpath(LINK_PRIZE_SIZE).text
        prize_size = str(re.sub('\D', '', prize))
    except Exception as e:
        print("can't get prize now", str(e))
        logging.exception("can't get prize by the link")
        return '0'
    logging.info('Prize extracted from competition page')
    return prize_size.replace(',', '')


def get_organizator_name(driver):
    """
   extract organizator name from competition page
   :param driver: chrome driver
   :return: str organizator name
   """
    try:
        organizator = driver.find_element_by_xpath(LINK_ORGANIZATOR_NAME).text

    except Exception as e:
        print("organizator can't get now", str(e))
        logging.exception("Can't get `organizator_name` from competition page")
        organizator = None

    logging.info("Collected`organizator_name` from competition page")
    return organizator


def get_number_of_topics(driver):
    """
    extract  number of topics from competition/ page
    :param driver: chrome driver
    :return: int number of topics
    """
    try:
        topics = driver.find_element_by_xpath(LINK_TOPIC).get_attribute("innerHTML")
        number_topics = str(re.sub('\D', '', topics))
    except Exception as e:
        print("topics: can't get now", str(e))
        logging.exception("Can't get `num_topics` from competition page")
        return '0'

    logging.info("Collected `num_topics` from competition page")
    return number_topics.replace(',', '')


if __name__ == '__main__':
    test_driver = create_driver()
    get_prize_size(test_driver)

    get_organizator_name(test_driver)

    get_number_of_topics(test_driver)

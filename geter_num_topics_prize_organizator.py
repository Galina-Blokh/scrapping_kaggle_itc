import re
from selenium import webdriver
import config

logger = config.get_logger(__name__)


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    driver.get("https://www.kaggle.com/c/m5-forecasting-accuracy/discussion")
    return driver


def get_prize_size(driver):
    """
   extract prize size from competition page
   :param driver: chrome driver
   :return: int prize size
   """
    try:
        prize = driver.find_element_by_xpath(config.LINK_PRIZE_SIZE).text
        prize_size = str(re.sub('\D', '', prize))
    except Exception as e:
        logger.debug("Can't get `prize` for the link" + str(e))
        return '0'
    logger.debug('`Prize` extracted from competition page')
    return prize_size.replace(',', '')


def get_organizator_name(driver):
    """
   extract organizator name from competition page
   :param driver: chrome driver
   :return: str organizator name
   """
    try:
        organizator = driver.find_element_by_xpath(config.LINK_ORGANIZATOR_NAME).text

    except Exception as e:
        logger.debug("Can't get `organizator_name` from competition page" + str(e))
        organizator = None

    logger.debug("Collected `organizator_name` from competition page")
    return organizator


def get_number_of_topics(driver):
    """
    extract  number of topics from competition/ page
    :param driver: chrome driver
    :return: str number of topics
    """
    try:
        topics = driver.find_element_by_xpath(config.LINK_TOPIC).get_attribute("innerHTML")
        number_topics = str(re.sub('\D', '', topics))
    except Exception as e:
        logger.debug("Can't get `num_topics` from competition page" + str(e))
        return '0'

    logger.debug("Collected `num_topics` from competition page")
    return number_topics.replace(',', '')


if __name__ == '__main__':
    test_driver = create_driver()
    get_prize_size(test_driver)
    get_organizator_name(test_driver)
    get_number_of_topics(test_driver)
    logger.info("Main in geter_num_topics_prize_organizator.py is finished")

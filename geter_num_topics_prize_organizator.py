import re
from selenium import webdriver
import config
from selenium.webdriver.firefox.options import Options

logger = config.get_logger(__name__)


def create_driver():
    """
    create selenium firefox  driver
    :return: driver
    """
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=r'./geckodriver')
    logger.info('Firefox driver was created')
    return driver


def get_prize_size(driver):
    """
   extract prize size from competition page
   :param driver: firefox driver
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
   :param driver: firefox driver
   :return: str organizator name
   """
    try:
        organizator = driver.find_element_by_xpath(config.LINK_ORGANIZATOR_NAME).text

    except Exception as e:
        logger.debug("Can't get `organizator_name` from competition page" + str(e))
        organizator = None

    logger.debug("Collected `organizator_name` from competition page")
    return organizator


if __name__ == '__main__':
    test_driver = create_driver()
    get_prize_size(test_driver)
    get_organizator_name(test_driver)
    logger.info("Main in geter_num_topics_prize_organizator.py is finished")

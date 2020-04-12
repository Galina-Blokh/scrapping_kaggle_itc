from selenium import webdriver
import time
import config

logger = config.get_logger(__name__)


def create_driver():
    """
    create silenium chrome driver
    :return: driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    return driver


def get_from_tag(driver, number):
    """
    get tag by number
    :param driver: selenium driver
    :param number: tag number
    :return: string
    """
    try:
        xpath = '//*[@id="site-content"]/div[2]/div/div[3]/div/div/div/div[2]/span[' + str(number) +\
                                      ']/div/a/span'
        tag = driver.find_element_by_xpath(xpath).text

    except Exception as e:
        # print("can't get now tag {}".format(str(number)))
        logger.info("can't get tag " + str(number))
        tag = None
    return tag


def extract_for_tags(driver):
    """
    collect tags from competition pages
    :param driver: chrome driver
    :return: list of dictionaries with extracted data
    """
    try:
        table = driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[3]/div/div/div/div[2]')
    except:
        logger.info("Can't find tags on the page")
        return []

    num_tags = len(table.find_elements_by_tag_name("a"))
    tags = []
    for i in range(1, num_tags+1):
        time.sleep(0.1)
        tag = get_from_tag(driver, i)
        tags.append(tag)

    logger.debug('Tags are extracted')
    return tags





import datetime
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('log_task.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler(sys.stdout))

COMPETITORS_TEXT_XPATH = '//*[@id="site-content"]/div[2]/div/div[2]/div[4]/div[1]/div[2]/p[2]'

def extract_competitors(driver):
    """
    extract number of competitors from competition page
    :param driver: chrome driver
    :return: number of competitors
    """
    try:
        if driver.find_element_by_xpath(COMPETITORS_TEXT_XPATH).text != 'Competitors':
            return '0'

        competitors = int(driver.find_element_by_xpath(
            '//*[@id="site-content"]/div[2]/div/div[2]/div[4]/div[1]/div[2]/p[1]').text)
    except:
        print('competitors: not now')
        logger.warning("Can't find `number competitors` on the page")
        competitors = '0'
    logger.info('Collected `number competitors` from page')
    return competitors


def extract_teams(driver):
    """
    extract number of teams from competition page
    :param driver: chrome driver
    :return: number of teams
    """
    try:
        teams = int(driver.find_element_by_xpath(
            '//*[@id="site-content"]/div[2]/div/div[2]/div[4]/div[1]/div[1]/p[1]').text)
    except:
        print('teams: not now')
        logger.warning("Can't collect `number teams`from a page")
        teams = '0'
    logger.info('Collected `number of teams` from competition page')
    return teams


def extract_header(driver):
    """
    extract header from competition page
    :param driver: chrome driver
    :return: number of teams
    """
    try:
        # header new style path
        header_competition = driver.find_element_by_xpath(
            '//*[@id="site-content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/h1').text
    except:
        try:
            # header old style path
            header_competition = driver.find_element_by_xpath(
                '//*[@id="site-content"]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div/h1').text
        except:
            print('header: not now')
            logger.warning("Can't collect `header` from competition page")
            return None
    logger.info("Collected `header` from competition page")
    return header_competition.replace("\"", "\\\"")


def get_number_of_entries(driver):
    """
    extract  number of entries from competition page
    :param driver: chrome driver
    :return: number of entries
    """
    entries_xpath = '//*[@id="site-content"]/div[2]/div/div[2]/div[4]/div[1]/div[3]/p[1]/span'
    try:
        if driver.find_element_by_xpath(COMPETITORS_TEXT_XPATH).text != 'Competitors':
            entries_xpath = '//*[@id="site-content"]/div[2]/div/div[2]/div[4]/div[1]/div[2]/p[1]/span'

        num_of_entries = driver.find_element_by_xpath(entries_xpath).text

    except:
        print('entries: not now')
        logger.warning('Cannot get `number of entries` from competition page')
        return '0'

    logger.info('Collected `number of entries` from competition page')
    return num_of_entries.replace(',','')


def get_description_of_competition(driver):
    """
    extract description from competition page
    :param driver: chrome driver
    :return: description
    """
    try:
        description_text = driver.find_element_by_xpath('//*[@id="competition-overview__nav-content-container"]/div[2]/div/div').text
    except:
        # print('description: not now')
        logger.warning('Cannot get `description` from competition page')
        return None

    logger.info('Collected `description` from competition page')
    return description_text.replace("\"", "\\\"")


def to_sql_datetime(date_str):
    '''
    convert string into datetime format
    :param date_str:
    :return: datetime obj
    '''
    date_time_obj = datetime.datetime.strptime(date_str, "%b %d, %Y")
    logger.info('Converted `date_str` into datetime obj')
    return date_time_obj.strftime("%Y-%m-%d")


def get_start_of_competition(driver):
    '''
    get competiton start
    :param driver: chrome driver
    :return: start date as str
    '''
    try:
        date_start = driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[2]/div[3]/div/div/div/div/div/div[3]/div[2]/span')
    except:
        logger.warning("Can't get `date_start of the competiton`. return '1900-01-01'")
        return '1900-01-01'
    logger.info('Got the `date_start` of the competiton')
    return to_sql_datetime(date_start.get_attribute('data-tooltip'))


def get_end_of_competition(driver):
    '''
       get competiton end
       :param driver: chrome driver
       :return: end date as str
       '''
    try:
        date_end = driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[2]/div[3]/div/div/div/div/div/div[4]/div[2]/span')
    except:
        try:
            #try to get copmetiton_end data for competitons whith deadline and competitions end with different dates
            date_end = driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[2]/div[3]/div/div/div/div/div/div[5]/div[2]/span')
        except:
            # print('date end: not now')
            logger.warning("Can't get `date_end of the competiton`. return '1900-01-01'")
            return '1900-01-01'
    logger.info('Got the `date_end` of the competiton')
    return to_sql_datetime(date_end.get_attribute('data-tooltip'))




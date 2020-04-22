import config
from selenium import webdriver
import time
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


def get_from_leaderboard(driver, row, column, column_name):
    """
    get data from one cell in leader board
    :param driver: chromedriver
    :param row: row number
    :param column: column number
    :param column_name: column name
    :return: text from cell
    """
    try:
        xpath = '//*[@id="site-content"]/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr[' + str(row) + ' ]/td[' \
                + str(column) + ']'
        data = driver.find_element_by_xpath(xpath).text

    except Exception as e:
        logger.debug("Can't get column from `leaderboard` " + column_name + str(e))
        data = str(0)
    logger.debug('Column from `leaderboard` is collected ' + column_name)
    return data


def extract_from_table(driver, link, current_leaderboard_dic, num_leaders):
    """
    extract data from leaderboard table
    :param driver: chromedriver
    :param link: link to competition leadreboard
    :param current_leaderboard_dic: dict of leaderboard features
    :param num_leaders: number of leader in table
    :return: list of dictionaries
    """
    leader_board = []
    for i in range(1, num_leaders - 1):
        time.sleep(0.1)
        res_dic = {"link": link.strip()}
        for key, value in current_leaderboard_dic.items():
            res_dic[key] = get_from_leaderboard(driver, i, value, key)
        leader_board.append(res_dic)
        logger.debug("row " + str(i) + " collected from " + link)
    logger.info('Extracted leader board data for link ' + link)
    return leader_board


def extract_for_leaderboard(links, driver):
    """
    extract leaderboard data for competition pages
    :param links: list of links to kaggle competitions pages
    :param driver: chrome driver
    :return: list of dictionaries with extracted data
    """
    logger.info("Extracting leader board data...")
    leader_board = []

    for link in links:
        try:
            driver.get(link + "/leaderboard")
            time.sleep(1)
        except Exception as e:
            logger.info("Can't get link:  " + link + "/leaderboard")
            continue

        try:
            table = driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[2]/div/div[2]/div/table')
        except Exception as e:
            logger.info("Can't find `leaderbord` table by the `link` " + link)
            continue

        # detect leaderboard table type
        try:
            if driver.find_element_by_xpath(config.SCORE_XPATH).text == 'Score':
                current_leaderboard_dic = config.LEADERBOARD_DICT_T1
            else:
                current_leaderboard_dic = config.LEADERBOARD_DICT_T2
        except Exception as e:
            logger.warning('Malformed leaderbord table ' + link)
            continue

        num_leaders = len(table.find_elements_by_tag_name("tr"))

        leader_board += extract_from_table(driver, link, current_leaderboard_dic, num_leaders)
    logger.info('Finished extracting `leaderboards`')
    return leader_board


if __name__ == '__main__':
    LINKS_LEADERBOARD_TEST = ['https://www.kaggle.com/c/passenger-screening-algorithm-challenge',
                              'https://www.kaggle.com/c/second-annual-data-science-bowl',
                              'https://www.kaggle.com/c/hospital',
                              'https://www.kaggle.com/c/deloitte-western-australia-rental-prices']

    chrome_driver = create_driver()

    logger.info('Main in the `leaderboards` finished')

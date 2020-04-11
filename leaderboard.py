import logging

from selenium import webdriver
import time
logging.basicConfig(filename='main.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def create_driver():
    """
    create silenium chrome driver
    :return: driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    return driver


LEADERBOARD_DICT_T1 = {'place': 1,  'team_name': 3, 'score': 6, 'entries_leader': 7, 'last_entry': 8}
LEADERBOARD_DICT_T2 = {'place': 1,  'team_name': 2, 'score': 5, 'entries_leader': 6, 'last_entry': 7}

SCORE_XPATH = '//*[@id="site-content"]/div[2]/div/div[2]/div/div[2]/div/table/thead/tr/th[6]/span/span'

def get_from_leaderboard(driver, row, column, column_name):
    try:
        xpath = '//*[@id="site-content"]/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr[' + str(row) + ' ]/td[' + str(column) + ']'
        data = driver.find_element_by_xpath(xpath).text

    except Exception as e:
        print("can't get now", column_name, str(e))
        logging.exception("can't get column from leaderboard")
        data = None
    logging.info('Whole row from leaderboard is collected')
    return data


def extract_for_leaderboard(links, driver):
    """
    collect data from competition pages
    :param links: list of links to kaggle competitions pages
    :param driver: chrome driver
    :return: list of dictionaries with extracted data
    """
    logging.info("Extracting leader board data...")
    leader_board = []

    for link in links:
        driver.get(link+"/leaderboard")
        time.sleep(2)

        try:
            table = driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[2]/div/div[2]/div/table')
        except Exception as e:
            print('Cant find leaderbord table', link)
            logging.exception('Cant find leaderbord table by the link')
            continue

        # detect leaderboard table type
        try:
            if driver.find_element_by_xpath(SCORE_XPATH).text == 'Score':
                curent_leaderboard_dic = LEADERBOARD_DICT_T1
            else:
                curent_leaderboard_dic = LEADERBOARD_DICT_T2
        except Exception as e:
            print('Malformed leaderbord table', link)
            logging.exception('Malformed leaderbord table')
            continue

        num_leaders = len(table.find_elements_by_tag_name("tr"))
        print(link, num_leaders )
        logging.info('point on the page with columns leaderbord table is founded')

        for i in range(1, num_leaders-1):
            time.sleep(0.1)
            res_dic = {"link": link.strip()}
            for key, value in curent_leaderboard_dic.items():
                res_dic[key] = get_from_leaderboard(driver, i, value, key)
            leader_board.append(res_dic)
            print(res_dic)
    logging.info('Extracting data from leaderboard  into dictionary is finished')
    return leader_board


if __name__ == '__main__':


    LINKS_LEADERBOARD_TEST = ['https://www.kaggle.com/c/passenger-screening-algorithm-challenge',
                              'https://www.kaggle.com/c/second-annual-data-science-bowl',
                              'https://www.kaggle.com/c/hospital',
                              'https://www.kaggle.com/c/deloitte-western-australia-rental-prices']

    chrome_driver = create_driver()

    print(extract_for_leaderboard(LINKS_LEADERBOARD_TEST, chrome_driver))
    logging.info('Main in the leaderboards finished work')


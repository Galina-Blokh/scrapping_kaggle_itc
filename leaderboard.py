from selenium import webdriver
import time


def create_driver():
    """
    create silenium chrome driver
    :return: driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    return driver


LEADERBOARD_DICT = {'place': 1, "position_change": 2, 'team_name': 3, 'score': 6, 'entries_leader': 7, 'last_entry': 8}


def get_from_leaderboard(driver, row, column, column_name):
    try:
        xpath = '//*[@id="site-content"]/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr[' \
                + str(row) + ' ]/td[' + str(column) + ']'
        data = driver.find_element_by_xpath(xpath).text

    except Exception as e:
        print("can't get now", column_name, str(e))
        data = None
    return data


def extract_for_leaderboard(links, driver):
    """
    collect data from competition pages
    :param links: list of links to kaggle competitions pages
    :param driver: chrome driver
    :return: list of dictionaries with extracted data
    """
    print("Extracting leader board data...")
    leader_board = []

    for link in links:
        driver.get(link+"/leaderboard")
        time.sleep(2)

        try:
            table = driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[2]/div/div[2]/div/table')
        except Exception as e:
            print('leaderbord problem', link)
            continue

        num_leaders = len(table.find_elements_by_tag_name("tr"))
        print(link, num_leaders )
        for i in range(1, num_leaders-1):
            time.sleep(0.1)
            res_dic = {"link": link.strip()}
            for key, value in LEADERBOARD_DICT.items():
                res_dic[key] = get_from_leaderboard(driver, i, value, key)
            leader_board.append(res_dic)
            print(res_dic)
    return leader_board


if __name__ == '__main__':
    LINKS_LEADERBOARD_TEST = ['https://www.kaggle.com/c/passenger-screening-algorithm-challenge',
                              'https://www.kaggle.com/c/second-annual-data-science-bowl',
                              'https://www.kaggle.com/c/hospital',
                              'https://www.kaggle.com/c/deloitte-western-australia-rental-prices']

    chrome_driver = create_driver()

    print(extract_for_leaderboard(LINKS_LEADERBOARD_TEST, chrome_driver))


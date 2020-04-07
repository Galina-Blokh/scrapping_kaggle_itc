from selenium import webdriver
import time
import csv
import download_one as do


def create_driver():
    """
    create silenium chrome driver
    :return: driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    return driver




def get_from_tag(driver, row):
    try:
        xpath = '//*[@id="site-content"]/div[2]/div/div[3]/div/div/div/div[2]/span['+ str(row) +\
                                      ']/div/a/span'
        tag = driver.find_element_by_xpath(xpath).text

    except Exception as e:
        print("can't get now tag {}".format(str(row)))
        tag = None
    return tag



def extract_for_tags(link, driver):
    """
    collect data from competition pages
    :param links: list of links to kaggle competitions pages
    :param driver: chrome driver
    :return: list of dictionaries with extracted data
    """
    print("Extracting tag data...")
    table = driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[3]/div/div/div/div[2]')
    num_tags = len(table.find_elements_by_tag_name("a"))
    tags = []
    for i in range(1, num_tags+1):
        time.sleep(0.1)
        tag = get_from_tag(driver, i)
        tags.append(tag)
    return tags




def main():
    LINKS_LEADERBOARD_TEST = ['https://www.kaggle.com/c/passenger-screening-algorithm-challenge',
                              'https://www.kaggle.com/c/second-annual-data-science-bowl',
                              'https://www.kaggle.com/c/hospital',
                              'https://www.kaggle.com/c/deloitte-western-australia-rental-prices']

    chrome_driver = create_driver()
    links = LINKS_LEADERBOARD_TEST
    for link in links:
        chrome_driver.get(link)
        time.sleep(2)
        tags = extract_for_tags(link, chrome_driver)
        print(link, tags)

if __name__ == '__main__':
    main()


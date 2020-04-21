import logging
import sys
from selenium import webdriver
import time
import argparse
from selenium.webdriver.firefox.options import Options

def get_links_from_page(my_webpage):
    """
    get links for competitions from one page
    :param my_webpage: link to page for scrapping
    :return: links from one page
    """
    competition_links = []
    for i in range(1, 20):
        try:
            compet = my_webpage.find_element_by_xpath(
                '//*[@id="root"]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/a[' + str(i) + ']')
        except:
            # print('not now')
            logger.exception("Can't get link id= " + str(i))
            continue
        competition_links.append(compet.get_attribute("href"))
    logger.debug('Collected competition links from one page')
    return competition_links


def connect():
    """
    create firefox driver
    :return: firefox  driver
    """
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=r'./geckodriver')
    driver.get("https://www.kaggle.com/search?q=in%3Acompetitions")
    time.sleep(5)
    logger.info('Firefox driver was created. Connected to kaggle')
    return driver


def get_links_from_site(driver, num_pages=450):
    """
    get competition links from kaggle site
    :param driver: firefox  driver
    :param num_pages: number of pages to scrap
    :return: list of links
    """
    competition_links = []
    for i in range(num_pages):
        competition_links += get_links_from_page(driver)
        logger.info('Collected `links` from page ' + str(i+1))
        driver.find_element_by_xpath(
            '//*[@id="root"]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[3]/div/button[2]').click()
        time.sleep(5)
    logger.info('Collected all competition links from pages')
    return competition_links


def extract_links_to_file(file_name):
    """
    extract links to .txt file
    :param file_name: output filename
    :return: nothing
    """
    kaggle_driver = connect()
    competition_links = get_links_from_site(kaggle_driver)
    output_comp_links = open(file_name, 'w')
    for link in competition_links:
        output_comp_links.write(link + '\n')
    output_comp_links.close()
    logger.info('Save link to file finished')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Exctract links for competitions from kaggle.com')

    parser.add_argument('--links_file', type=str, help='Where store the scrapped links of competitions', action="store",
                        default='kaggle_links.txt')
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('get_links.log')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    logger.info("Start to collect competition links from Kaggle.com")
    extract_links_to_file(args.links_file)
    logger.info("Main in get_links.py is finished")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


#Header of project
# //*[@id="site-content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/h1

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='kaggle_itc/chromedriver')
    return driver


def get_header(driver):
    try:
        # header new style path
        header_competition = driver.find_element_by_xpath(
            '//*[@id="site-content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/h1').text
        print('header: OK', header_competition)
    except:
        try:
            # header old style path
            header_competition = driver.find_element_by_xpath(
                '//*[@id="site-content"]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div/h1').text
        except:
            print('header: not now')
            header_competition = None

    return header_competition


def extract_headers(links, driver):
    header_list = []
    for link in links:
        driver.get(link)
        time.sleep(3)
        header_list.append([link, get_header(driver)])

    return header_list


def extract_links_headers_to_file(links, output_filename, driver):
    headers = open(output_filename, 'w')
    for element in extract_headers(links, driver):
        headers.write(element[0] + ',' + element[1] + '\n')
        headers.close()


if __name__ == '__main__':
    links_file = open('competition_links_5p.txt', "r")
    chrome_driver = create_driver()
    extract_links_headers_to_file(links_file.readlines(), 'header_links.txt', chrome_driver)





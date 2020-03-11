from selenium import webdriver
import time

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    return driver

def get_competitors(driver):
    try:
        competitors = driver.find_element_by_xpath(
            '//*[@id="site-content"]/div[2]/div/div[2]/div[4]/div[1]/div[2]/p[1]').text
        print('competitors: OK', competitors)
    except:
        print('competitors: not now')
        competitors = None
    return competitors


def extract_competitors(links, driver):
    competitors_list = []
    for link in links:
        driver.get(link)
        time.sleep(3)
        competitors_list.append([link, get_competitors(driver)])
    return competitors_list


def extract_links_competitors_to_file(links, output_filename, driver):
    competitors = open(output_filename, 'w')
    for element in extract_competitors(links, driver):
        competitors.write(element[0] + ',' + element[1] + '\n')
        competitors.close()


if __name__ == '__main__':
    links_file = open('competition_links_5p.txt', "r")
    chrome_driver = create_driver()
    extract_links_competitors_to_file(links_file.readlines(), 'competitors.txt', chrome_driver)



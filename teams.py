from selenium import webdriver
import time

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='kaggle_itc/chromedriver')
    return driver

def get_teams(driver):
    try:
        teams = driver.find_element_by_xpath(
            '//*[@id="site-content"]/div[2]/div/div[2]/div[4]/div[1]/div[1]/p[1]').text
        print('teams: OK', teams)
    except:
        print('teams: not now')
        teams = None
    return teams


def extract_teams(links, driver):
    teams_list = []
    for link in links:
        driver.get(link)
        time.sleep(3)
        teams_list.append([link, get_teams(driver)])
    return teams_list


def extract_links_teams_to_file(links, output_filename, driver):
    teams = open(output_filename, 'w')
    for element in extract_teams(links, driver):
        teams.write(element[0] + ',' + element[1] + '\n')
        teams.close()


if __name__ == '__main__':
    links_file = open('competition_links_5p.txt', "r")
    chrome_driver = create_driver()
    extract_links_teams_to_file(links_file.readlines(), 'teams.txt', chrome_driver)



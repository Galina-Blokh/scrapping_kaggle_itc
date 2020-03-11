from selenium import webdriver
import time
import csv


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    return driver


def extract_competitors(driver):
    try:
        competitors = driver.find_element_by_xpath(
            '//*[@id="site-content"]/div[2]/div/div[2]/div[4]/div[1]/div[2]/p[1]').text
        print('competitors: OK', competitors)
    except:
        print('competitors: not now')
        competitors = None
    return competitors


def extract_teams(driver):
    try:
        teams = driver.find_element_by_xpath(
            '//*[@id="site-content"]/div[2]/div/div[2]/div[4]/div[1]/div[1]/p[1]').text
        print('teams: OK', teams)
    except:
        print('teams: not now')
        teams = None
    return teams


def extract_header(driver):
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
            print('header: OK', header_competition)
        except:
            print('header: not now')
            header_competition = None

    return header_competition


def extract_for_competition(links, driver):
    competition_info = []

    for link in links:
        driver.get(link)
        time.sleep(3)
        res_dic = {"link": link.strip()}
        for key, value in COMPETITION_FEATS.items():
            res_dic[key] = value(driver)
        competition_info.append(res_dic)
    return competition_info


def dicts_to_csv(list_of_dicts, output_filename):
    writer = csv.DictWriter(open(output_filename, "w", newline=''), fieldnames=list_of_dicts[0].keys())
    writer.writeheader()
    for row in list_of_dicts:
        writer.writerow(row)


if __name__ == '__main__':
    COMPETITION_FEATS = {"get_header": extract_header, "get_teams": extract_teams, "get_compet": extract_competitors}
    chrome_driver = create_driver()
    competition_data = extract_for_competition(open('competition_links_5p.txt', "r").readlines(), chrome_driver)
    dicts_to_csv(competition_data, 'kaggle_competition.csv')

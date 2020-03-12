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


def extract_for_competition(links, driver):
    """
    collect data from competition pages
    :param links: list of links to kaggle competitions pages
    :param driver: chrome driver
    :return: list of dictionaries with extracted data
    """
    competition_info = []

    for link in links:
        driver.get(link)
        time.sleep(2)
        res_dic = {"link": link.strip()}
        for key, value in COMPETITION_FEATS.items():
            res_dic[key] = value(driver)
        print(res_dic)
        competition_info.append(res_dic)
    return competition_info


def dicts_to_csv(list_of_dicts, output_filename):
    """
    save list of dictionaries to .csv file
    :param list_of_dicts: list of dictionaries
    :param output_filename:name for output .csv file
    :return: none
    """
    writer = csv.DictWriter(open(output_filename, "w", newline=''), fieldnames=list_of_dicts[0].keys())
    writer.writeheader()
    for row in list_of_dicts:
        writer.writerow(row)


if __name__ == '__main__':
    print("Hi! I'm starting to exctract data about kaggle competitions")

    COMPETITION_FEATS = {"header": do.extract_header, "competition_start": do.get_start_of_competition,
                         "competition_end": do.get_end_of_competition,
                         "teams": do.extract_teams, "competitors": do.extract_competitors, "entries": do.get_number_of_entries,
                         "description": do.get_description_of_competition}
    chrome_driver = create_driver()
    competition_data = extract_for_competition(open('competition_links_5p.txt', "r").readlines(), chrome_driver)
    dicts_to_csv(competition_data, 'kaggle_competition.csv')

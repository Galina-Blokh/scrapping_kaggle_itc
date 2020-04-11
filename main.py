import sys
from selenium import webdriver
import json
import time
import csv
import download_one as do
import leaderboard

import tags
import geter_num_topics_prize_organizator as tpo
import logging



def create_driver():
    """
    create silenium chrome driver
    :return: driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    logger.info('Chromedriver is created')
    return driver


def extract_for_competition(links, driver):
    """
    collect data from competition pages
    :param links: list of links to kaggle competitions pages
    :param driver: chrome driver
    :return: list of dictionaries with extracted data; dictionary with tags
    """
    logger.info("Extracting competition data...")
    competition_info = []
    tags_dic = {}

    for link in links:
        driver.get(link)
        time.sleep(2)
        res_dic = {"link": link.strip()}
        for key, value in COMPETITION_FEATS.items():
            res_dic[key] = value(driver)
        try:
            tags_dic[link.strip()] = tags.extract_for_tags(driver)
        except Exception as e:
            # print("tags problem", link, e)
            logger.warning("tags problem with the link")

        driver.get(link + "/discussion")
        time.sleep(1)
        res_dic["number_topics"] = tpo.get_number_of_topics(driver)
        # print(res_dic)
        competition_info.append(res_dic)
        logger.debug(res_dic)
    logger.info('number_topics is added into result dictionary')
    return competition_info, tags_dic


def dicts_to_csv(list_of_dicts, output_filename):
    """
    save list of dictionaries to .csv file
    :param list_of_dicts: list of dictionaries
    :param output_filename:name for output .csv file
    :return: none
    """
    writer = csv.DictWriter(open(output_filename, "w", newline='', encoding="utf-8"),
                            fieldnames=list_of_dicts[0].keys())
    writer.writeheader()
    for row in list_of_dicts:
        writer.writerow(row)
    logger.info('the dictionary/json file is converted into csv {}'.format(output_filename))


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('log_task.log')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    logger.info("Hi! I'm starting to exctract data about kaggle competitions")

    COMPETITION_FEATS = {"header": do.extract_header, "competition_start": do.get_start_of_competition,
                         "competition_end": do.get_end_of_competition,
                         "teams_count": do.extract_teams, "competitors": do.extract_competitors,
                         "entries_competition": do.get_number_of_entries,
                         "description": do.get_description_of_competition, "prize": tpo.get_prize_size,
                         "organizator_name": tpo.get_organizator_name}

    chrome_driver = create_driver()
    links = open('test_links.txt', "r").readlines()

    competitions_data, tags_data = extract_for_competition(links, chrome_driver)
    dicts_to_csv(competitions_data, 'kaggle_competition.csv')

    leader_board = leaderboard.extract_for_leaderboard(links, chrome_driver)
    dicts_to_csv(leader_board, 'kaggle_leaders.csv')

    with open('tags.json', 'w') as file:
        json.dump(tags_data, file)
    logger.info('main in the main is finished')

import config
from selenium import webdriver
import json
import time
import csv
import download_one as do
import leaderboard
import tags
import geter_num_topics_prize_organizator as tpo
import argparse
import kaggle_api


def create_driver():
    """
    create selenium chrome driver
    :return: driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    logger.info('Chromedriver was created')
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
            logger.info("Extracting `tags` for " + link)
        except Exception as e:
            logger.debug("no `tags` for `link` " + link + str(e))

        driver.get(link + "/discussion")
        time.sleep(1)

        res_dic["number_topics"] = do.extract_number_topic(driver)

        competition_info.append(res_dic)
        logger.info("Collected data for `link` " + link)

    logger.info('Collected data for `competitions`.')
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
    logger.info('The dictionary/json file saved into csv {}'.format(output_filename))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract data from kaggle.com')

    parser.add_argument('--links_file', type=str, help='File with links to competition pages', action="store",
                        default='test_links.txt')
    parser.add_argument('--compet_file', type=str, help='Where to store data from competition page',
                        default='kaggle_competition.csv')
    parser.add_argument('--leader_file', type=str, help='Where to store data from leadreboard page',
                        default='kaggle_leaders.csv')
    parser.add_argument('--tags_file', type=str, help='Where to store tags from competition page',
                        default='tags.json')
    parser.add_argument('--competitions_api_file', type=str, help='Where to store data for competitions from API',
                        default='competitions_api_file.csv')
    parser.add_argument('--kernels_file', type=str, help='Where to store kernels from competition page',
                        default='kernels_file.csv')

    args = parser.parse_args()

    logger = config.get_logger(__name__)

    logger.info("Hi! I'm starting to extract data about kaggle competitions")

    COMPETITION_FEATS = {"header": do.extract_header, "competition_start": do.get_start_of_competition,
                         "competition_end": do.get_end_of_competition,
                         "teams_count": do.extract_teams, "competitors": do.extract_competitors,
                         "entries_competition": do.get_number_of_entries,
                         "description": do.get_description_of_competition, "prize": tpo.get_prize_size,
                         "organizator_name": tpo.get_organizator_name}

    chrome_driver = create_driver()
    competition_links = open(args.links_file, "r").readlines()

    competitions_data, tags_data = extract_for_competition(competition_links, chrome_driver)
    dicts_to_csv(competitions_data, args.compet_file)

    leader_board = leaderboard.extract_for_leaderboard(competition_links, chrome_driver)
    dicts_to_csv(leader_board, args.leader_file)

    competitions_api, kernels = kaggle_api.competitions_new_search()
    dicts_to_csv(competitions_api, args.competitions_api_file)
    dicts_to_csv(kernels, args.kernels_file)

    with open(args.tags_file, 'w') as file:
        json.dump(tags_data, file)

    logger.info('Scrapping is finished')

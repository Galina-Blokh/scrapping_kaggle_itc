import logging
import sys

LOG_FILE = 'download.log'
COMPETITORS_TEXT_XPATH = '//*[@id="site-content"]/div[2]/div/div[2]/div[4]/div[1]/div[2]/p[2]'
LINK_PRIZE_SIZE = '''//*[@id="site-content"]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div[2]'''
LINK_ORGANIZATOR_NAME = '''//*[@id="site-content"]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[3]/div/ul/li[1]/span/span[2]'''
LINK_TOPIC = '''//*[@id="site-content"]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/span'''
LEADERBOARD_DICT_T1 = {'place': 1, 'team_name': 3, 'score': 6, 'entries_leader': 7, 'last_entry': 8}
LEADERBOARD_DICT_T2 = {'place': 1, 'team_name': 2, 'score': 5, 'entries_leader': 6, 'last_entry': 7}
SCORE_XPATH = '//*[@id="site-content"]/div[2]/div/div[2]/div/div[2]/div/table/thead/tr/th[6]/span/span'
BASE_URL = 'https://www.kaggle.com/c/'


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger

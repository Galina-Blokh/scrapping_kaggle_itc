import sys
from kaggle.api.kaggle_api_extended import KaggleApi

from download_one import logger


def competitions_new_search():
    """ Searching competitions
     creates api connection and takes competitions data by all existing pages
     :returns dict of new competitions
     """
    api = KaggleApi()
    api.authenticate()
    i = 0
    list_compet_new = []
    while True:
        competitions = api.competitions_list(category="all", page=i)
        print('page {}'.format(i))
        # competitions is a list of competition objects.
        # iterate though each item to access individual competition
        # #date = datetime obj
        for comp in competitions:
            list_compet_new.append(
                {'ref': str(comp.ref).replace('-', ' '), 'prize': comp.reward, 'userRank': str(comp.userRank),
                 'deadline': str(comp.deadline), 'category': comp.category, 'team_count': str(comp.teamCount),
                 'userHasEntered': str(int(comp.userHasEntered))})
        i+=1
        if len(competitions) == 0:
            print('download complete')
            return list_compet_new


def main():
    """prints call of the functions"""
    listic =competitions_new_search()
    for item in listic:
        print(item)


if __name__ == '__main__':
    main()

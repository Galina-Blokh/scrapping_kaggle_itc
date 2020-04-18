import re
import sys
from kaggle.api.kaggle_api_extended import KaggleApi
import config

logger = config.get_logger(__name__)


def competitions_new_search():
    """ Searching competitions
     creates api connection and takes competitions data by all existing pages
     :returns dict of new competitions
     """
    logger.info('competitions_new_search starts to create New_data dictionary  for competition ')

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
            d = {'url': comp.url,
                 'title': str(comp.title),
                 'description': comp.description,
                 'prize': str(comp.reward).replace('$','').replace(',',''),
                 'enabledDate': str(comp.enabledDate),
                 'deadline': str(comp.deadline),
                 'category': comp.category,
                 'team_count': str(comp.teamCount),
                 'userHasEntered': str(int(comp.userHasEntered)),
                 'organizator': str(comp.organizationName),
                 'maxDailySubmissions': str(comp.maxDailySubmissions),
                 'tags': str(comp.tags)}
            if d['tags'] == '[]':
                d['tags'] = '0'
            try:
                str(int(d['prize']))
            except:
                d['prize'] = '0'

            list_compet_new.append(d)
        i += 1
        if len(competitions) == 0:
            print('download complete')
            logger.info('New_data dictionary  for competition is created')
            return list_compet_new





def main():
    """prints call of the functions"""
    listic = competitions_new_search()
    for item in listic:
        print(item)


if __name__ == '__main__':
    main()

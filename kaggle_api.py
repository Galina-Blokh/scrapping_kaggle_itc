from kaggle.api.kaggle_api_extended import KaggleApi
import config

logger = config.get_logger(__name__)


def get_kenel_for_compet(compet_ref, api):
    """
    Get information about kernels for competition
    :param compet_ref: competition name
    :param api: kernel api
    :return: list of dictionaries
    """
    kernels = api.kernels_list(search=compet_ref)
    kernel_list = []
    for kernel in kernels:
        kernel_list.append({'link': config.BASE_URL + compet_ref,
                            'author': kernel.author,
                            'name': kernel.title,
                            'votes': kernel.totalVotes})

    logger.debug('Collected `kernels` from page')

    return kernel_list


def competitions_new_search():
    """ Searching competitions
     creates api connection and takes competitions data by all existing pages
     :returns list of dict  new competitions and list of dict  kernels
     """
    logger.info('competitions_new_search starts to create New_data dictionary  for competition ')

    api = KaggleApi()
    api.authenticate()
    i = 0
    list_compet_new = []
    kernel_for_compet = []
    while True:
        competitions = api.competitions_list(category="all", page=i)
        print('page {}'.format(i))
        # competitions is a list of competition objects.
        # iterate though each item to access individual competition
        for comp in competitions:
            d = {'link': comp.url,
                 'title': str(comp.title),
                 'description': comp.description,
                 'prize': str(comp.reward).replace('$', '').replace(',', ''),
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
            kernel_for_compet += get_kenel_for_compet(comp.ref, api)
        i += 1
        if len(competitions) == 0:
            logger.info("New Data using Kaggle API is collected")
            return list_compet_new, kernel_for_compet


def main():
    """prints call of the functions"""
    competitions_new_search()
    logger.info("Main in kaggle_api.py is finished")



if __name__ == '__main__':
    main()

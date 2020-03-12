def extract_competitors(driver):
    """
    extract number of competitors from competition page
    :param driver: chrome driver
    :return: number of competitors
    """
    try:
        competitors = int(driver.find_element_by_xpath(
            '//*[@id="site-content"]/div[2]/div/div[2]/div[4]/div[1]/div[2]/p[1]').text)
    except:
        print('competitors: not now')
        competitors = None
    return competitors


def extract_teams(driver):
    """
    extract number of teams from competition page
    :param driver: chrome driver
    :return: number of teams
    """
    try:
        teams = int(driver.find_element_by_xpath(
            '//*[@id="site-content"]/div[2]/div/div[2]/div[4]/div[1]/div[1]/p[1]').text)
    except:
        print('teams: not now')
        teams = None
    return teams


def extract_header(driver):
    """
    extract header from competition page
    :param driver: chrome driver
    :return: number of teams
    """
    try:
        # header new style path
        header_competition = driver.find_element_by_xpath(
            '//*[@id="site-content"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/h1').text
    except:
        try:
            # header old style path
            header_competition = driver.find_element_by_xpath(
                '//*[@id="site-content"]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div/h1').text
        except:
            print('header: not now')
            header_competition = None

    return header_competition


def get_number_of_entries(driver):
    """
    extract  number of entries from competition page
    :param driver: chrome driver
    :return: number of entries
    """
    try:
        num_of_entries = driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[2]/div[4]/div[1]/div[3]/p[1]/span').text

    except:
        print('entries: not now')
        num_of_entries = None
    return num_of_entries


def get_description_of_competition(driver):
    """
    extract description from competition page
    :param driver: chrome driver
    :return: description
    """
    try:
        description_text = driver.find_element_by_xpath('//*[@id="competition-overview__nav-content-container"]/div[2]/div/div').text
    except:
        print('description: not now')
        description_text = None
    return description_text


def get_start_of_competition(driver):
    try:
        date_start = driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[2]/div[3]/div/div/div/div/div/div[3]/div[2]/span')
    except:
        print('date start: not now')
        return None
    return date_start.get_attribute('data-tooltip')


def get_end_of_competition(driver):
    try:
        date_end = driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[2]/div[3]/div/div/div/div/div/div[4]/div[2]/span')
    except:
        print('date end: not now')
        return None
    return date_end.get_attribute('data-tooltip')




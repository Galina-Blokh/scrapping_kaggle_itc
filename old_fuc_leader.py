
def extract_place(driver, i):
    try:
        xpath = '//*[@id="site-content"]/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr[' + str(i) +']/td[1]'
        place = int(driver.find_element_by_xpath(xpath).text)
    except Exception as e:
        print('place: not now', str(e), xpath)
        place = None
    return place


def extract_position_change(driver, i):
    try:
        position_change = int(driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr[' + str(i) +']/td[2]').text)
    except:
        print('position_change: not now')
        position_change = None
    return position_change


def extract_team_name(driver, i):
    try:
        team_name = str(driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr[' + str(i) +']/td[3]').text)
    except Exception as e:
        print('team_name: not now', str(e))
        team_name = None
    return team_name


def extract_score(driver, i):
    try:
        score = float(driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr[' + str(i) +']/td[6]').text)

    except Exception as e:
        print('score: not now', str(e))
        score = None
    return score

def extract_entries_leader(driver, i):
    try:
        entries_leader = str(driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr[' + str(i) +']/td[7]').text)
    except:
        print('entries_leader: not now')
        entries_leader = None
    return entries_leader


def extract_last_entry(driver, i):
    try:
        last_entry = str(driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr[' + str(i) +']/td[8]').text)
    except:
        print('last_entry: not now')
        last_entry = None
    return last_entry


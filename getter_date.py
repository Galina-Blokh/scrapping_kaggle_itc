from selenium import webdriver
import time
import datetime
import sys

NUMBER_OF_ARGS = 2

LINK_END = '//*[@id="site-content"]/div[2]/div/div[2]/div[3]/div/div/div/div/div/div[4]/div[2]/span'
LINK_BEGIN ='//*[@id="site-content"]/div[2]/div/div[2]/div[3]/div/div/div/div/div/div[3]/div[2]/span'
LINK_COMPETITION ='https://www.kaggle.com/c/info-290t-who-survived-the-titanic/overview/evaluation'



def create_driver():
    """
    creates driver to get the link
    :return: driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    return driver


def get_date_of_competition(driver, link_competition):
    """
    gets date of the start and the end of the competition
    :param driver:
    :return: list of two elements
    """
    list_of_dates = []
    driver.get(link_competition)
    time.sleep(3)
    date_end = driver.find_element_by_xpath(LINK_END)
    date_start = driver.find_element_by_xpath(LINK_BEGIN)
    date_s = (date_start.get_attribute('data-tooltip'))
    date_e = date_end.get_attribute('data-tooltip')
    list_of_dates.append(date_s)
    list_of_dates.append(date_e)
    return list_of_dates


def write_date_into_file(list_of_dates):
    try:
        with open('date_file.txt', 'a+') as daf:
            [daf.write(i) for i in list_of_dates]
            print(list_of_dates)
        return "date_file.txt created"
    except:
        sys.exit('cant create a date_file.txt')


def getting_duration_competition(date_str_file):
    """
    get the path or the name of the file
    reads from a file list of two dates and counting the delta
    :param date_str_file:
    :return: datetime duration_competition
    """
    try:
        with open(date_str_file, 'r+') as dsf:
            dates = dsf.readlines()
            duration_competition = datetime.datetime.strptime(dates[1], '%b %d, %Y\n') - datetime.datetime.strptime(
                dates[0], '%b %d, %Y\n')
            return duration_competition
    except:
        sys.exit('cant read a file')


def main():
    if len(sys.argv) != NUMBER_OF_ARGS:
        print('usage: ./convertor.py link_competition')
        sys.exit(1)

    link_competition = sys.argv[1]

    chrome_driver = create_driver()
    list_of_dates = get_date_of_competition(chrome_driver, link_competition)
    for i in list_of_dates:
        write_date_into_file(i + '\n')


    print(getting_duration_competition('date_file.txt'))




if __name__ == '__main__':
    main()

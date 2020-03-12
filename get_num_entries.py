from selenium import webdriver
import sys

NUMBER_OF_ARGS = 2
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



def get_number_of_entries(driver, link_competition):
    """
    :param driver:
    :param link_competition:
    :return: str number of entries in this competition
    """
    driver.get(link_competition)
    num_of_entries = driver.find_element_by_xpath('//*[@id="site-content"]/div[2]/div/div[2]/div[4]/div[1]/div[3]/p[1]/span').text
    return num_of_entries





def main():
    """
    accepts arg from command line
    prints the res of  get_number_of_entries(create_driver(),link_competition)
    """
    if len(sys.argv) != NUMBER_OF_ARGS:
        print('usage: ./get_num_entries.py link_competition')
        sys.exit(1)

    link_competition = sys.argv[1]
    print(get_number_of_entries(create_driver(),link_competition))



if __name__ == '__main__':
    main()

from selenium import webdriver
import sys

NUMBER_OF_ARGS = 2
LINK_COMPETITION ='https://www.kaggle.com/c/info-290t-who-survived-the-titanic/overview/description'

def create_driver():
    """
    creates driver to get the link
    :return: driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    return driver



def get_description_of_competition(driver, link_competition):
    """
    :param driver:
    :param link_competition:
    :return: str text of element description
    """
    driver.get(link_competition)
    description_text = driver.find_element_by_xpath('//*[@id="competition-overview__nav-content-container"]/div[2]/div/div').text
    return description_text





def main():
    """
    accepts arg from command line
    prints the res of  get_number_of_entries(create_driver(),link_competition)
    """
    if len(sys.argv) != NUMBER_OF_ARGS:
        print('usage: ./convertor.py link_competition')
        sys.exit(1)

    link_competition = sys.argv[1]
    print(get_description_of_competition(create_driver(),link_competition))



if __name__ == '__main__':
    main()

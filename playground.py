from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def get_page():
    for i in range(1, 20):
        try:
            compet = driver.find_element_by_xpath(
                '//*[@id="root"]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/a[' + str(i) + ']')
        except:
            print('not now')
            continue
        competition_links.append(compet.get_attribute("href"))


options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(chrome_options=options, executable_path='kaggle_itc/chromedriver')
driver.get("https://www.kaggle.com/search?q=in%3Acompetitions")
time.sleep(5)
assert "Kaggle" in driver.title

competition_links = []


for i in range(1,10):
    get_page()
    # click button next page
    driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[3]/div/button[2]').click()
    time.sleep(5)


print(competition_links)





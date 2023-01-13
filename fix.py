from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import pickle

path = 'C:/Users/eduar/chromedriver.exe'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)
web = 'https://web.archive.org/web/20221115040351/https://en.wikipedia.org/wiki/2022_FIFA_World_Cup'

def missingData():


    driver.get(web)
    #while(True):
    #    pass

    matches = driver.find_elements(by='xpath', value='//td[@align="right"]/.. | //td[@style="text-align:right;"]/.. | //tr[@itemprop="name"]')

    home = []
    score = []
    away = []
    for match in matches:
        home.append(match.find_element(by='xpath', value='./th[1]/span | ./td[1]').text)
        score.append(match.find_element(by='xpath', value='./th[2] | ./td[2]').text)
        away.append(match.find_element(by='xpath', value='./th[3]/span/span | ./th[3]/span | ./td[3]').text)

    dict_football = {'home': home, 'score': score, 'away': away}
    df_football = pd.DataFrame(dict_football)
    df_football['year'] = 2022
    time.sleep(2)
    return df_football


df_fixture = missingData()
print(df_fixture)



df_fixture.to_csv('2022fixture2.csv', index=False)
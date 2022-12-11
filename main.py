from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
path = 'C:/Users/eduar/chromedriver.exe'


service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)


def missingData(year):

    web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'
    driver.get(web)
    #while(True):
    #    pass
    if year < 1970 or year > 1998:
        matches = driver.find_elements(by='xpath',
                                       value='//tr[@itemprop="name"]')
    else:
        matches = driver.find_elements(by='xpath', value='//td[@align="right"]/.. | //td[@style="text-align:right;"]/..')

    home = []
    score = []
    away = []
    for match in matches:
        home.append(match.find_element(by='xpath', value='./th[1]/span | ./td[1]').text)
        score.append(match.find_element(by='xpath', value='./th[2] | ./td[2]').text)
        away.append(match.find_element(by='xpath', value='./th[3]/span/span | ./td[3]').text)

    dict_football = {'home': home, 'score': score, 'away': away}
    df_football = pd.DataFrame(dict_football)
    df_football['year'] = year
    time.sleep(2)
    return df_football

years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018]
#years = [1930, 2006, 2010, 2014, 2018]


fifa = [missingData(year) for year in years]
driver.quit()
df_fifa = pd.concat(fifa, ignore_index=True)
df_fifa.to_csv('fifacupsdata.csv', index=False)
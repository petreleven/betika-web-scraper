from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import pickle
import pandas as pd


web = 'https://www.betika.com/s/soccer'
path="C:\\pythonScripts\\geckodriver.exe"
options=Options()
options.add_argument('--headless')
driver=webdriver.Firefox(executable_path=path,service_log_path='nul')
driver.get(web)

teams=[]
x12=[]
btts=[]
odds_events=[]

def scroll_page():
    htmlElem=driver.find_element_by_tag_name('html')
    for i in range (1,15,1):
        htmlElem.send_keys(Keys.END)
        time.sleep(2)
        continue


def dropdown_menu():
    dropdowns=driver.find_elements_by_class_name('match-filter')
    dropdown_button=dropdowns[3]
    dropdown_button.click()
    btts_button=driver.find_elements_by_class_name('match-filter__group__action')
    time.sleep(3)
    btts_button[3].click()


def x_12(x12):
    sport_title=driver.find_elements_by_class_name('prebet-match')
    for game in sport_title:
        team=game.find_element_by_class_name('prebet-match__teams')
        teams.append(team.text)

        odd=game.find_element_by_class_name('prebet-match__odds')
        x12.append(odd.text)


def both_teams_to_score(btts):
    dropdown_menu()
    time.sleep(3)
    scroll_page()
    sport_title=driver.find_elements_by_class_name('prebet-match')
    for game in sport_title:
        odd=game.find_element_by_class_name('prebet-match__odds__container')
        btts.append(odd.text)

scroll_page()
x_12(x12)
both_teams_to_score(btts)
driver.quit()

'''CLEANING DATA'''
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)


dict_gambling={'Teams':teams,'3-Way':x12}
df_betika=pd.DataFrame.from_dict(dict_gambling)
df_betika=df_betika.applymap(lambda x:x.strip() if isinstance(x,str) else x)

'''SAVE DATA'''
output=open('df_betika','wb')
pickle.dump(df_betika,output)
output.close()
print(df_betika)
print(len(btts))


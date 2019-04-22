import requests                   
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions 
import re
import time
import pickle



# Get ids of the papers

ids = []
i=0



for i in range(0,223):
    page = requests.get("https://papers.ssrn.com/sol3/JELJOUR_Results.cfm?npage="+str(i+1)+"&form_name=journalBrowse&journal_id=179252&Network=yes&lim=false")
    if page.status_code==200:      
        soup = BeautifulSoup(page.content, 'html.parser')
    for j in range(0,50): 
        ids.append(soup.select('div.tbody div.trow.abs')[j]['id'].strip('div_'))



def remove_duplicate(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list



ids = remove_duplicate(ids)



with open("ids.txt", "wb") as fp:   #Pickling
    pickle.dump(ids, fp)



with open("ids.txt", "rb") as fp:   # Unpickling
    ids = pickle.load(fp)



# Path where you save the webdriver 
executable_path = 'chromedriver.exe'

# initiator the webdriver for Firefox or Chrome browser
driver = webdriver.Chrome(executable_path=executable_path)

driver.get('https://hq.ssrn.com/login/pubsigninjoin.cfm')

# Sign in to the SSRN website
username = driver.find_element_by_name("input-email")
password = driver.find_element_by_name("input-pass")

username.send_keys("<enter your SSRN registered email id>")
password.send_keys("<Enter your SSRN password>")

driver.find_element_by_id("signinBtn").click()




# Download pdf's
# Download pdf's
for i in ids[10000:11150]:
    try:
        #driver.implicitly_wait(60)
        driver.get('https://papers.ssrn.com/sol3/papers.cfm?abstract_id='+i)
        time.sleep(1.5)
        driver.find_elements_by_id('downloadPdf')[0].click()
        time.sleep(0.75)
    except:
        pass
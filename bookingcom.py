from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
from selenium.webdriver.common.action_chains import ActionChains

global comp
file_json = {}
ordah = 1
filtering = 0
cty = 'SURABAYA'

chrome = r'D:\chrome\chromedriver.exe'
driver_web = webdriver.Chrome(chrome)

while True:
    try:
        driver_web.get('https://www.booking.com/')
        WebDriverWait(driver_web, 2).until(EC.presence_of_element_located((By.XPATH,"//input[@name='ss']")))
        break
    except:
        print('Timeout')
        continue

searchBar = driver_web.find_element_by_xpath("//input[@name='ss']")
searchBar.send_keys(cty)
searchBar.send_keys(Keys.ENTER)
        
element = WebDriverWait(driver_web, 10).until(EC.presence_of_element_located((By.ID, "hotellist_inner")))
total_old = driver_web.find_element_by_id('basiclayout').find_element_by_class_name('sorth1').text
num_old = total_old.split(':')[1].strip().split(' ')[0]

##INPUT
while(1):
    try:
        input_1 = 4
        if input_1 == 3:
            filter_btn = driver_web.find_element_by_id('filter_class').find_element_by_class_name('filteroptions').find_element_by_xpath('a[3]/label/div').click()
        elif input_1 == 4:
            filter_btn = driver_web.find_element_by_id('filter_class').find_element_by_class_name('filteroptions').find_element_by_xpath('a[4]/label/div').click()
        elif input_1 == 5:
            filter_btn = driver_web.find_element_by_id('filter_class').find_element_by_class_name('filteroptions').find_element_by_xpath('a[5]/label/div').click()
        else:
            driver_web.quit()
        filtering = 1
        break
    except:
        continue

if filtering == 1:
    while (1):
    #     try:
        file_json[cty] = []
        print('masokk')
        element_1 = WebDriverWait(driver_web, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "sr-usp-overlay__container")))
        max_per_page = driver_web.find_element_by_id('basiclayout').find_element_by_class_name('bui-pagination__info').text
        total_new = driver_web.find_element_by_id('basiclayout').find_element_by_class_name('sorth1').text
        num_nw = total_new.split(':')[1].strip().split(' ')[0]
        nx_step = int(int(num_nw)/int(max_per_page.split('–')[1].strip()))
        if num_nw != num_old: 
            print(num_nw)
            for br in range (nx_step+1):
                print('Step - '+ str(br+1))
                element_1 = WebDriverWait(driver_web, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "sr-usp-overlay__container")))
    #             element_1 = WebDriverWait(driver_web, 5).until(EC.presence_of_element_located((By.ID, "hotellist_inner")))
                kk = driver_web.find_element_by_id('hotellist_inner')
                scores = kk.find_elements_by_xpath('div')
                for score in range (len(scores)):
                    if scores[score].get_attribute('data-class') == None:
                        comp = 0
                    else:
                        comp = 1

                    element = WebDriverWait(driver_web, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sr-hotel__title-badges")))

                    if comp == 1:
                        hotel = scores[score].find_element_by_class_name('sr-hotel__name')
                        url = scores[score].find_element_by_tag_name('a')

                        new_tab = scores[score].find_element_by_tag_name('a').click()
                        driver_web.switch_to.window(driver_web.window_handles[1])
                        element_1 = WebDriverWait(driver_web, 10).until(EC.element_to_be_clickable((By.ID,"property_description_content")))
                        addr = driver_web.find_element_by_id('hotelTmpl').find_element_by_tag_name('p').text.split('–')[0].strip()
                        print(driver_web.find_element_by_id('hotelTmpl').find_element_by_tag_name('p').text.split('–')[0].strip())
                        driver_web.close()
                        driver_web.switch_to.window(driver_web.window_handles[0])

                        star = scores[score].find_element_by_class_name('sr-hotel__title-badges')
                        if scores[score].get_attribute('data-score') == None or scores[score].get_attribute('data-score') == '':
                            if star.text == '' or star.text == None:
                                print(str(ordah)+' '+hotel.text+' '+url.get_attribute('href'))
                                file_json[cty].append({
                                    'Hotel Name' : hotel.text,
                                    'Address' : addr,
                                    'URL' : url.get_attribute('href')
                                })
                            else:
                                print(str(ordah)+' '+hotel.text+' '+star.text+' '+addr+' '+url.get_attribute('href'))
                                file_json[cty].append({
                                    'Hotel Name' : hotel.text,
                                    'Star' : star.text,
                                    'Address' : addr,
                                    'URL' : url.get_attribute('href')
                                })
                        else:
                            if star.text == '' or star.text == None:
                                print(str(ordah)+' '+hotel.text+' '+scores[score].get_attribute('data-score')+' '+url.get_attribute('href'))
                                file_json[cty].append({
                                    'Hotel Name' : hotel.text,
                                    'Score' : scores[score].get_attribute('data-score'),
                                    'Address' : addr,
                                    'URL' : url.get_attribute('href')
                                })
                            else:
                                print(str(ordah)+' '+hotel.text+' '+star.text+' '+scores[score].get_attribute('data-score')+' '+url.get_attribute('href'))
                                file_json[cty].append({
                                    'Hotel Name' : hotel.text,
                                    'Star' : star.text,
                                    'Score' : scores[score].get_attribute('data-score'),
                                    'Address' : addr,
                                    'URL' : url.get_attribute('href')
                                })

                        ordah += 1  

                    else:

                        pass                            
                    
                time.sleep(1)
                if br == nx_step:
                    driver_web.quit()
                    break
                else:
                    nx_bttn = driver_web.find_element_by_xpath('//*[@id="search_results_table"]/div[4]/nav/ul/li[3]/a').click()
                    time.sleep(1)
                    print('\n\n')

            break

        else:

            continue
            
else:
    
    pass
            
print(json.dumps(file_json, indent=2))
with open(cty+'.txt', 'w') as f:
    json.dump(file_json, f)

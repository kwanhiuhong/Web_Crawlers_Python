#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 16:52:05 2018

@author: KHH
"""
#%%
##Scraping financial data using Selenium, import packages first
import pandas as pd
from numpy import nan
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#%%
#if you set the range to be 2000, then the csv/dataframe will finally have 2000 rows
df = pd.DataFrame(index=range(2000),
                  columns=['University_name', 'Ranking', 'Country', 
                           'Source'])

#%% 
## launch the Chrome browser, please change directory to the location of your Chromedriver exe file and save that as my_path
my_path = r"/Users/hiuhongkwan/Documents/Developer_Tools/Chrome_Driver/chromedriver"
browser = webdriver.Chrome(executable_path=my_path)
browser.maximize_window()

url_form = "https://www.usnews.com/education/best-global-universities/rankings?page={}" 
#the id name of button next  =  "qs-rankings_next"
#%%

#This is to scrap USNEWS
#here to select how many pages you want to scrap, if set 11, then only 10 pages be scrapped
#for this project, since we have to scrap 1000 university, we should set it to 101
#each page in USNews contains 10 university
page_number = [no for no in range(1,101)]

university = []
ranking = []
country = []
source = []
 
for i, page_no in enumerate(page_number):
    url = url_form.format(page_no)
    browser.get(url)
    for count in range(10):
        count2 = count + 1;
        university_xpath = "//div[@id='resultsMain']/div[1]/div["+str(count2)+"]"+"/div[@class='block unwrap']/h2[@class='h-taut']/a"
        ranking_xpath = "//div[@id='resultsMain']/div[1]/div["+str(count2)+"]"+"/div[2]/span[contains(text(), '#')]"
        country_xpath = "//div[@id='resultsMain']/div[1]/div["+str(count2)+"]"+"/div[@class='block unwrap']/div[@class='t-taut']/span[1]"
        try:
            university.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, university_xpath))).text)
            ranking.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, ranking_xpath))).text)
            country.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, country_xpath))).text)
            source.append("USNEWS")
        #if the web doesn't respond within 10 seconds. then just goto except:
        except:
            university.append(nan)
            ranking.append(nan)
            country.append(nan)
            source.append(nan)
print(university)

#here!!!!, if you choose to scrap 100 pages in line 39, then in total 100 university be scrapped
#for this project, we have to scrap 1000, so I you should set to 1000 in the following line.
for i in range(1000):
    df.loc[i, "University_name"] = university[i]
    df.loc[i, "Ranking"] = ranking[i]
    df.loc[i, "Country"] = country[i]
    df.loc[i, "Source"] = source[i]


#This is to scrap QS rankings
url_QS = "https://www.topuniversities.com/university-rankings/world-university-rankings/2018"
browser.get(url_QS)
#since every page in QS contains 25 universities, if you want to scrap 1000 universities, then the number in
#the following line should be 40, and actually for QS, there are only 960 universities, other blank place be filled with nan
for count in range(40):
    for universities_per_page in range(25):
        universities_every_page = universities_per_page + 1
        university_xpath = "//tbody[1]/tr["+str(universities_every_page)+"]"+"/td[2]/div/a[@class='title']"
        ranking_xpath = "//tbody[1]/tr["+str(universities_every_page)+"]"+"/td[1]/div/div[1]/span[2]"
        country_xpath = "//tbody[1]/tr["+str(universities_every_page)+"]"+"/td[3]/div/img"
        try:
            university.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, university_xpath))).text)
            ranking.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, ranking_xpath))).text)
            country.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, country_xpath))).get_attribute("alt"))
            source.append("QS")
#if the web doesn't respond within 10 seconds. then just goto except:
        except:
            university.append(nan)
            ranking.append(nan)
            country.append(nan)
            source.append(nan)
#the element here used to scroll to the position containing the next page button so
# that "click" function can perform, it won't perform if the next page button doesn't show on the page
# even the html code may have already generated.
    try:
#for the page there are only 959 universities.
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody[1]/tr[24]"+"/td[2]/div/a[@class='title']")))
        browser.execute_script("arguments[0].scrollIntoView();", element)
        #WebDriverWait(browser, 10).until(browser.execute_script("arguments[0].scrollIntoView();", element))
        button_for_next_page_id = 'qs-rankings_next'
        button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, button_for_next_page_id)))
        button.click()
    except:
        break
#if this program reaches the final page of QS ranking, it waits around 5 minutes to stop running the 
#program, I don't know why but it's the case
#fill the remaining 1000 rows.
for i in range(1000,2000):
    try:
        df.loc[i, "University_name"] = university[i]
        df.loc[i, "Ranking"] = ranking[i]
        df.loc[i, "Country"] = country[i]
        df.loc[i, "Source"] = source[i]
    except:
        df.loc[i, "University_name"] = nan
        df.loc[i, "Ranking"] = nan
        df.loc[i, "Country"] = nan
        df.loc[i, "Source"] = nan

browser.quit()
df.to_csv("University ranking.csv", index=False, encoding='utf_8_sig')

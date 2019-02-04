#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 23:04:13 2018

@author: KHH
"""

import pandas as pd
from numpy import nan
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

df = pd.DataFrame(index=range(20000),
                  columns=['City', 'Date', 'AQI', 'Range', 
                           'Air quality level', 'PM2.5', 'PM10', 'SO2', 'CO', 'NO2','O3'])

my_path = r"/Users/KHH/Desktop/ChromeDriver_for_web_scrapping/chromedriver"
browser = webdriver.Chrome(executable_path=my_path)
browser.maximize_window()

url_form = "https://www.aqistudy.cn/historydata/monthdata.php?city={}" 

Cities_to_scrap = []

city_in_excel = []
date = []
aqi = []
Range = []
air_quality_level = []
PM2_point_5 = []
PM10 = []
SO2 = []
CO = []
NO2 = []
O3 = []

url = "https://www.aqistudy.cn/historydata"
browser.get(url)

#This part is to scrap the total cities for accessing respective cities' pages
#after successfully scrapping, total cities would be around 383
Cities_to_scrap_xpath = "//div[@class='all']/div[@class='bottom']/ul"
for i in range(1,len(browser.find_elements_by_xpath(Cities_to_scrap_xpath))+1):
    Cities_in_alphabetic_order_xpath = "//div[@class='all']/div[@class='bottom']/ul["+str(i)+']'+'/div[2]/li'
    for count2 in range(1,len(browser.find_elements_by_xpath(Cities_in_alphabetic_order_xpath))+1):
        Cities_in_alphabetic_order_xpath = "//div[@class='all']/div[@class='bottom']/ul["+str(i)+']'+'/div[2]/li['+str(count2)+']'+'/a'
        Cities_to_scrap.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, Cities_in_alphabetic_order_xpath))).text)
    
#This part scraps individual cities air quality information

for i, city in enumerate(Cities_to_scrap):
    url_for_specific_city = url_form.format(city)
    browser.get(url_for_specific_city)
    #WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "table table-condensed table-bordered table-striped table-hover table-responsive")))
    #!!!!since the page is rather dynamic, when you open the link, the table/html doesn't render
    #immediately, so i set it to wait for 6 seconds for the whole page to load, if you think your
    #internet is faster, you can set it to a shorter time.
    time.sleep(7)
    air_quality_table_xpath = "//table[@class='table table-condensed table-bordered table-striped table-hover table-responsive']/tbody[1]/tr"
    #here finds how many rows are there for that particular city
    for air_quality_row in range(2, len(browser.find_elements_by_xpath(air_quality_table_xpath))+1):
        date_xpath = "//tbody[1]/tr["+str(air_quality_row)+']'+"/td[1]/a"
        aqi_xpath = "//tbody[1]/tr["+str(air_quality_row)+']'+"/td[2]"
        Range_xpath = "//tbody[1]/tr["+str(air_quality_row)+']'+"/td[3]"
        air_quality_level_xpath = "//tbody[1]/tr["+str(air_quality_row)+']'+"/td[4]/span"
        PM2_point_5_xpath = "//tbody[1]/tr["+str(air_quality_row)+']'+"/td[5]"
        PM10_xpath = "//tbody[1]/tr["+str(air_quality_row)+']'+"/td[6]"
        SO2_xpath = "//tbody[1]/tr["+str(air_quality_row)+']'+"/td[7]"
        CO_xpath = "//tbody[1]/tr["+str(air_quality_row)+']'+"/td[8]"
        NO2_xpath = "//tbody[1]/tr["+str(air_quality_row)+']'+"/td[9]"
        O3_xpath = "//tbody[1]/tr["+str(air_quality_row)+']'+"/td[10]"
        try:
            city_in_excel.append(city)
            date.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, date_xpath))).text)
            aqi.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, aqi_xpath))).text)
            Range.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, Range_xpath))).text)
            air_quality_level.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, air_quality_level_xpath))).text)
            PM2_point_5.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, PM2_point_5_xpath))).text)
            PM10.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, PM10_xpath))).text)
            SO2.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, SO2_xpath))).text)
            CO.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, CO_xpath))).text)
            NO2.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, NO2_xpath))).text)
            O3.append(WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, O3_xpath))).text)
        except:
            city_in_excel.append(nan)
            date.append(nan)
            aqi.append(nan)
            Range.append(nan)
            air_quality_level.append(nan)
            PM2_point_5.append(nan)
            PM10.append(nan)
            SO2.append(nan)
            CO.append(nan)
            NO2.append(nan)
            O3.append(nan)


for count5 in range(0, len(city_in_excel)):
    df.loc[count5, "City"] = city_in_excel[count5]
    df.loc[count5, "Date"] = date[count5]
    df.loc[count5, "AQI"] = aqi[count5]
    df.loc[count5, "Range"] = Range[count5]
    df.loc[count5, "Air quality level"] = air_quality_level[count5]
    df.loc[count5, "PM2.5"] = PM2_point_5[count5]
    df.loc[count5, "PM10"] = PM10[count5]
    df.loc[count5, "SO2"] = SO2[count5]
    df.loc[count5, "CO"] = CO[count5]
    df.loc[count5, "NO2"] = NO2[count5]
    df.loc[count5, "O3"] = O3[count5]
        
browser.quit()    
df.to_csv("Air_Quality_KHH_3035375167.csv", index = False, encoding='utf_8_sig')

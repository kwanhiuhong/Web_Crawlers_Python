#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 10:01:23 2018

@author: KHH
"""

import pandas as pd
from numpy import nan
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#%%
df = pd.DataFrame(index=range(1000),
                  columns=['Brand Name', 'Discounted Price', 'Original Price', 
                           'Price Change'])

my_path = r"/Users/hiuhongkwan/Documents/Developer_Tools/Chrome_Driver/chromedriver"
browser = webdriver.Chrome(executable_path=my_path)
browser.maximize_window()

Brand_name = []
Discounted_price = []
Original_price = []
Price_change = []

url = "https://www.theoutnet.com/en-hk/shop/clothing/coats" 
browser.get(url)
time.sleep(10)
product_list_xpath= "//ul[@class='sr-product-list']/li"

for cnt in range(8):
    if(cnt != 0):
        ##please do not scoll the page when running this program!!
        #otherwise the click will not perform
        next_page_button_xpath = "//div[@class='right-tools']/div[1]/div[1]/div[2]/nav/ul[1]/li[@class='nextPage']"
        next_button = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH,next_page_button_xpath)))
        next_button.click()
        time.sleep(10)
    for count in range(1, len(browser.find_elements_by_xpath(product_list_xpath))+1):
        Brand_name_xpath = "//ul[@class='sr-product-list']/li["+str(count)+"]"+"/div[@class='wrapper']/a/div[@class='description product-details']/span[1]"
        Currency_xapth = "//ul[@class='sr-product-list']/li["+str(count)+"]"+"/div[@class='wrapper']/a/div[@class='description product-details']/div[@class='pricing']/div[@class='price']/span[1]/span/span[1]"
        Discounted_price_xpath = "//ul[@class='sr-product-list']/li["+str(count)+"]"+"/div[@class='wrapper']/a/div[@class='description product-details']/div[@class='pricing']/div[@class='price']/span[1]/span/span[2]"
        Original_price_xpath = "//ul[@class='sr-product-list']/li["+str(count)+"]"+"/div[@class='wrapper']/a/div[@class='description product-details']/div[@class='pricing']/div[@class='price']/span[@class='full price']/span[2]"
        Price_change_xpath = "//ul[@class='sr-product-list']/li["+str(count)+"]"+"/div[@class='wrapper']/a/div[@class='description product-details']/div[@class='pricing']/div[@class='price']/span[@class='markdown']"
        try:
            Brand_name.append(WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, Brand_name_xpath))).text)
            print (str(count)+" "+WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, Brand_name_xpath))).text)
            discounted_price_with_currency_sign = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, Currency_xapth))).text +" " + WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, Discounted_price_xpath))).text
            Discounted_price.append(discounted_price_with_currency_sign)
        except:
            Brand_name.append(nan)
            Discounted_price.append(nan)
        #since sometimes the original price and price change are not shown on the web
        #sometimes the area shows "EXCLUSIVE to the OUTNET" but not the original price, so I put
        #two try-and-except here.
        try:  
            original_price_with_currency_sign = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, Currency_xapth))).text +" " + WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, Original_price_xpath))).text
            Original_price.append(original_price_with_currency_sign)
            Price_change.append(WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, Price_change_xpath))).text)
        except:
            Original_price.append(nan)
            Price_change.append(nan)
            
for count2 in range(0, len(Brand_name)):
    df.loc[count2, 'Brand Name'] = Brand_name[count2]
    df.loc[count2, 'Discounted Price'] = Discounted_price[count2]
    df.loc[count2, 'Original Price'] = Original_price[count2]
    df.loc[count2, 'Price Change'] = Price_change[count2]

browser.quit()    
df.to_csv("Outnet_KHH_3035375167.csv", index = False, encoding='utf_8_sig')
#next_page_xpath = "//div[@class='right-tools']/div[1]/div[1]/div[2]/nav/ul[1]/li[@class='currentPage pageNumber']/a[1]/span[@class='text']"
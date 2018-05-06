#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 03:12:46 2018

@author: SaiSanthosh
"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ErrorInResponseException, StaleElementReferenceException
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import os, time, csv


#writing datafile to rt
rt=pd.read_csv('/Users/SaiSanthosh/Desktop/BIA660/Project/Final_Dataset.csv',encoding='latin-1')
rt.replace(r'\s+', np.nan, regex=True)
rt = rt.drop_duplicates(subset = 'Movie Name', keep = False)


start = 0



#Creating a file to write scraped data
if os.path.exists('test_budget1.csv'): 
    with open('test_budget1.csv','r') as fo: 
        
        start = len(fo.readlines())
    f=open('test_budget1.csv','a+')
else:
    f=open('test_budget1.csv','a+')
    


#Web Driver
ua=UserAgent()
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (ua.random)
service_args=['--ssl-protocol=any','--ignore-ssl-errors=true']
driver = webdriver.Chrome(desired_capabilities=dcap,service_args=service_args)


#creating dictionaries
budget = {}
weekend = {}
gross_us={}
gross_ww={}
    
def imdb_budget(movie_name, director):
   
    #To login into imdbpro
    driver.get('http://www.imdb.com/')
    
    #searches for login button
    imdbPro = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="navProMenu"]/p/a/img')))
    imdbPro.click()
    
    #clicks on imdblogin
    loginButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header_message"]/a')))
    loginButton.click()
    
    login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_with_imdb_expender"]')))
    login.click()
    
    ###entering login details
    driver.find_element_by_xpath('//*[@id="ap_email"]').send_keys('munna.saisanthosh@gmail.com')
    driver.find_element_by_xpath('//*[@id="ap_password"]').send_keys('Stevens_123')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="signInSubmit"]'))).click()
    
    x=start
    
    if os.path.exists('test_movie.txt'): 
        with open('test_movie.txt','r') as ko: 
            movie_list = ko.readlines()
            movie_list = set(movie_list)
            movielist = list(movie_list)

        k=open('test_movie.txt','a+')
    else:
        k=open('test_movie.txt','a+')

    #passing movie into loop 
    for n in movie_name[:].iterrows():
        o = n[1]['Title']+ '\n'
        if o in movielist:
            continue

        print(x+1)
        
        gross_us[x] = 'nan'
        gross_ww[x] = 'nan'
        budget[x] = 'nan'
        weekend[x] = 'nan'
        
        ####passing movie name
        if not driver.find_element_by_xpath('//*[@id="searchField"]'):
            driver.refresh()
            time.sleep(300)
            driver.refresh()
            time.sleep(200)
            driver.refresh()
            time.sleep(100)
            
            
        search = driver.find_element_by_xpath('//*[@id="searchField"]')
        search.clear()
        search.send_keys(n[1]['Title'])
        
        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search_container"]/form/a'))).click()
        #time.sleep(10)
        
        ### Refines search- selecting only movies
        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="TITLE"]'))).click() 
        try:
            WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="type"]/ul/li[1]/label'))).click()
        
        except TimeoutException:
            WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="type"]/ul/li[1]/label'))).click()
            
        time.sleep(2)
        global f
        try:
        ###clicks on first result
            numb = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.CLASS_NAME, "total_item_count"))).text
                                                                                        
            
            if numb == '0':
                
                f.write('\n'+str(x+1)+'\t'+str(n[1]['Title'])+'\t'+str(budget.get(x))+'\t'+str(weekend.get(x))+'\t'+str(gross_us.get(x))+'\t'+str(gross_ww.get(x)))
    
                k.write(str(n[1]['Title'])+'\n')
                x=x+1
                continue
                
            else:
                first=WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="results"]/ul/li[1]/ul/li[1]/span/a')))
                
                first.click()
    
                ###selects main details header where we have all info
                if driver.find_element_by_xpath('//*[@id="main_details"]'):
                    head = driver.find_element_by_xpath('//*[@id="main_details"]').text
                    #print(head)
                    new = head.split('\n')
                      
                    ###Sparsing data into required dictionary
                    for i in range(len(new)):
                        if new[i] == 'BUDGET':
                            b=new[i+1].split('(')
                            budget[x] = b[0]
    
                        if new[i] == 'OPENING WKD':
                            w = new[i+1].split('(')
                            weekend[x] = w[0]
    
                        if new[i] == 'GROSS':
                            if '|' in new[i+1]:
                                
                                g=new[i+1].split('|')
                                g1 = g[0].split('(')
                                g3=g1[0]
                                g2= g[1].split('(')
                                g4 = g2[0]
                            else:
                                g = new[i+1].split('(')
                                g3= g[0]
                                g4 = 'nan'
    
                            gross_us[x] = g3
                            gross_ww[x] = g4
                            
                    
                    f.write('\n'+str(x+1)+'\t'+str(n[1]['Title'])+'\t'+str(budget.get(x))+'\t'+str(weekend.get(x))+'\t'+str(gross_us.get(x))+'\t'+str(gross_ww.get(x)))
                    x=x+1
                    k.write(str(n[1]['Title'])+'\n')
                else:
                    f.write('\n'+str(x+1)+'\t'+str(n[1]['Title'])+'\t'+str(budget.get(x))+'\t'+str(weekend.get(x))+'\t'+str(gross_us.get(x))+'\t'+str(gross_ww.get(x)))
                    k.write(str(n[1]['Title'])+'\n')
                    x=x+1
                    continue
        
            
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            print('Exception')
            f.write('\n'+str(x+1)+'\t'+str(n[1]['Title'])+'\t'+str(budget.get(x))+'\t'+str(weekend.get(x))+'\t'+str(gross_us.get(x))+'\t'+str(gross_ww.get(x)))
            k.write(str(n[1]['Title'])+'\n')
            x=x+1
            continue
        
    
    k.close()
    #converting dictionaries to dataframes
    budget_df = pd.DataFrame([budget])
    weekend_df = pd.DataFrame([weekend])
    gross_us_df = pd.DataFrame([gross_us])
    gross_ww_df = pd.DataFrame([gross_ww])
  

    return budget_df,weekend_df,gross_us_df, gross_ww_df, x


def movienames_split(title):
    t=[]
    for name in title:
        if len(name) < 5:
            t.append(name)
        else:
            try:
                n1 = name.split('(')
                t.append(n1[0])
            except:
                t.append(np.nan)
            
    movie_name = pd.DataFrame([t])
    movie_name = movie_name.transpose()
    movie_name.columns = ['Title']
    
    return movie_name
 

     

movie_name = movienames_split(rt.loc[:,'Movie Name'])
budget, weekend, gross_us, gross_ww, final = imdb_budget(movie_name, rt.loc[:,'Directed By'])


#result = directors("Zack Snyder")

    
    
f.close()

#concatinating all the dictionaries
df1=pd.concat(( budget, weekend, gross_us, gross_ww), axis=0)
df1 = df1.transpose()
df= pd.DataFrame(columns=['Movie Title','budget', 'weekend', 'gross_us', 'gross_ww'])
df=pd.concat((movie_name['Title'][start:final],df1),axis=1)  

#writing all the scrapped data into excel file

if os.path.exists('imdb_budget.csv'): 
    with open('imdb_budget.csv', 'a+') as imdb:
        df.to_csv(imdb, header=False, na_rep = np.nan, encoding='utf-8')
else:
    with open('imdb_budget.csv', 'a+') as imdb:
        df.to_csv(imdb, header=True, na_rep = np.nan, encoding='utf-8')



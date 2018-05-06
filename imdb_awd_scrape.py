#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  6 18:38:10 2018

@author: SaiSanthosh
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 01:03:28 2018

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
import os, re, csv, time



###Function to get directors list
def directorslist(directors):
    first = directors.loc[:,'director1'].to_dict()
    second = directors.loc[:,'director2'].to_dict()
    
    
    final = {}
    
    x = 0
    for i in first.values():
        final[x] = i
        x = x+1
        
    for i in second.values():
        final[x] = i
        x=x+1

    
    direct = set(final.values())
    direct_list= list(direct)
    
    with open('test_directorlist.txt','a+') as f:
        for i in direct_list:
            f.write(str(i)+'\n')
    
    return direct_list




    
    
#function to get directors rank and awards
def directorstarmeter(direct_list):
    
    start = 0
    
    #creating dictionaries
    name_d = {}
    star_d = {}
    oscars_d = {}
    another_Wins_d = {}
    nominations_d = {}
    bignominations_d = {}
    
    if os.path.exists('test_dirlist.txt'): 
        with open('test_dirlist.txt','r') as ko: 
            dir_list = ko.readlines()
            dir_list = set(dir_list)
            dirlist = list(dir_list)
        k=open('test_dirlist.txt','a+')
    else:
        k=open('test_dirlist.txt','a+')
    
    if os.path.exists('test_director.txt'): 
        with open('test_director.txt','r') as fo: 
            start = len(fo.readlines())
        f=open('test_director.txt','a+')
    else:
        f=open('test_director.txt','a+')
        
            
    driver.get('http://www.imdb.com/')
    
    #searches for login button
    imdbPro = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="navProMenu"]/p/a/img')))
    imdbPro.click()
    
    #clicks on imdblogin
    loginButton = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header_message"]/a')))
    loginButton.click()
    
    login = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_with_imdb_expender"]')))
    login.click()
    
    ###entering login details
    driver.find_element_by_xpath('//*[@id="ap_email"]').send_keys('munna.saisanthosh@gmail.com')
    driver.find_element_by_xpath('//*[@id="ap_password"]').send_keys('Stevens_123')
    WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="signInSubmit"]'))).click()
    

    
    y=start
   
    #passing movie into loop 
    st = []
    for i in dirlist:
            st.append(str(i).strip())
       
    for n in direct_list[1:]:
        n = str(n).strip()
        if n in st:
            continue
        
        oscars_d[y] = 0
        another_Wins_d[y]=0
        nominations_d[y] = 0
        bignominations_d[y] = 0
        star_d[y] = 0    
        name_d[y] = n
        print(y+1)
            
            ####passing writer name
        if not driver.find_element_by_xpath('//*[@id="searchField"]'):
            driver.refresh()
            time.sleep(300)
            driver.refresh()
            time.sleep(200)
            driver.refresh()
            time.sleep(100)
            
            
        search = driver.find_element_by_xpath('//*[@id="searchField"]')
        search.clear()
        search.send_keys(n)
            
        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search_container"]/form/a'))).click()
        #time.sleep()
        
        ### Refines search- selecting only directors
        try:
            WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="NAME"]'))).click()
        except:
            WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="NAME"]'))).click()
            
        try:
            WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="profession"]/ul/li[3]/label'))).click()
        except TimeoutException:
            WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="profession"]/ul/li[3]/label'))).click()
        
        time.sleep(2)

            
        try:
            ###clicks on first result
            numb = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="title"]/div[1]/div/span[1]/span[1]'))).text
            
            if numb == '0':
                f.write('\n'+str(y+1)+'\t')
                f.write(str(n)+'\t')
                f.write(str(star_d.get(y))+'\t'+str(oscars_d.get(y))+'\t'+str(another_Wins_d.get(y))+'\t'+str(nominations_d.get(y))+'\t'+str(bignominations_d.get(y)))
                k.write('\n'+str(n))
                y=y+1
                continue
                    
            else:
                WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="results"]/ul/li[1]/ul/li[1]/span/a'))).click()
                rank = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="meter"]/span[1]/span[2]'))).text
                star_d[y] = rank
            
                if driver.find_element_by_xpath('//*[@id="main_details"]/div/div[1]/dl[1]/dd[2]'):
                    ###selects main details header where we have all info abt awards
                    head = driver.find_element_by_xpath('//*[@id="main_details"]/div/div[1]/dl[1]/dd[2]').text
                    #print(head)
                    new = head.split()
                    ###Sparsing data into required dictionary
                    for i in range(len(new)):
                        try:
                            if new[i] == 'Oscars.':
                                if not new[i-2] == 'for':
                                    oscars_d[y]=new[i-1]
                            elif new[i] == 'Oscar.':
                                if not new[i-2] == 'for':
                                    oscars_d[y] = new[i-1]
                            elif new[i] == 'wins':
                                another_Wins_d[y] = new[i-1]
                            elif new[i] == 'win':
                                another_Wins_d[y] = new[i-1]
                            elif new[i] == 'nominations':
                                nominations_d[y] = new[i-1]
                            elif new[i] == 'nomination':
                                nominations_d[y] = new[i-1]
                            elif new[i] == 'for':
                                bignominations_d[y] = new[i+1]
                                
                        except:
                            print('Exception')
                
                    f.write('\n'+str(y+1)+'\t')
                    f.write(str(n)+'\t')
                    f.write(str(star_d.get(y))+'\t'+str(oscars_d.get(y))+'\t'+str(another_Wins_d.get(y))+'\t'+str(nominations_d.get(y))+'\t'+str(bignominations_d.get(y)))
                    k.write('\n'+str(n))
                    
                    y=y+1
                else:
                    f.write('\n'+str(y+1)+'\t')
                    f.write(str(n)+'\t')
                    f.write(str(star_d.get(y))+'\t'+str(oscars_d.get(y))+'\t'+str(another_Wins_d.get(y))+'\t'+str(nominations_d.get(y))+'\t'+str(bignominations_d.get(y)))
                    k.write('\n'+str(n))
                    
                    y=y+1
                    continue
 
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            print('Exception')
            f.write('\n'+str(y+1)+'\t')
            f.write(str(n)+'\t')
            f.write(str(star_d.get(y))+'\t'+str(oscars_d.get(y))+'\t'+str(another_Wins_d.get(y))+'\t'+str(nominations_d.get(y))+'\t'+str(bignominations_d.get(y)))
            k.write('\n'+str(n))
            y=y+1
            continue
                
            
    k.close()   
    f.close()        
    name_d_df = pd.DataFrame([name_d])
    name_d_df = name_d_df.transpose()       
    rank_d_df = pd.DataFrame([star_d])
    rank_d_df = rank_d_df.transpose()
    oscars_d_df = pd.DataFrame([oscars_d])
    oscars_d_df = oscars_d_df.transpose()
    another_Wins_d_df = pd.DataFrame([another_Wins_d])
    another_Wins_d_df = another_Wins_d_df.transpose()
    nominations_d_df = pd.DataFrame([nominations_d])
    nominations_d_df = nominations_d_df.transpose()
    bignominations_d_df = pd.DataFrame([bignominations_d])
    bignominations_d_df = bignominations_d_df.transpose()
    
    return name_d_df ,rank_d_df, oscars_d_df, nominations_d_df, another_Wins_d_df, bignominations_d_df

###function to get writers list into set
def writerslist(writers):
    first = writers.loc[:,'writer1'].to_dict()
    second = writers.loc[:,'writer2'].to_dict()
    
    
    final = {}
    
    x = 0
    for i in first.values():
        final[x] = i
        x = x+1
        
    for i in second.values():
        final[x] = i
        x=x+1

    
    write = set(final.values())
    write_list= list(write)
    
    with open('test_writerlist.txt','a+') as f:
        for i in write_list:
            f.write(str(i) + '\n')
    
    return write_list





#function to get writers ranks and awards
def writerstarmeter(write_list):
    
    start = 0
    
    #creating dictionaries
    name_w = {}
    star_w = {}
    oscars_w = {}
    another_Wins_w = {}
    nominations_w = {}
    bignominations_w = {}
    
    if os.path.exists('test_writer_list.txt'): 
        with open('test_writer_list.txt','r') as ko: 
            writer = ko.readlines()
            writerlist = set(actlist)
            writerlist = list(actlist)
        k=open('test_actor_list.txt','a+')
    else:
        k=open('test_actor_list.txt','a+')
        
    if os.path.exists('test_writer.csv'): 
        with open('test_writer.csv','r') as fo: 
            start = len(fo.readlines())
        f=open('test_writer.csv','a+')
    else:
        f=open('test_writer.csv','a+')
        writer = csv.writer(f, fieldnames = ['name_w', 'rank_w', 'oscars_w', 'nominations_w', 'another_wins_w', 'bignominations_w'])
        writer.writeheader()
    
    driver.get('http://www.imdb.com/')
    
    #searches for login button
    imdbPro = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="navProMenu"]/p/a/img')))
    imdbPro.click()
    
    #clicks on imdblogin
    loginButton = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header_message"]/a')))
    loginButton.click()
    
    login = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_with_imdb_expender"]')))
    login.click()
    
    ###entering login details
    driver.find_element_by_xpath('//*[@id="ap_email"]').send_keys('munna.saisanthosh@gmail.com')
    driver.find_element_by_xpath('//*[@id="ap_password"]').send_keys('Stevens_123')
    WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="signInSubmit"]'))).click()
    

    
    y=start
   
        
    wt = []
    for i in writerlist:
            wt.append(str(i).strip())
            
    #passing movie into loop 
    for n in write_list[1:]:
        n = str(n).strip()
        if n in wt:
            continue
        
        oscars_w[y] = 0
        another_Wins_w[y]= 0
        nominations_w[y] = 0
        bignominations_w[y] = 0
        print(y+1)
            
        ####passing writer name
        if not driver.find_element_by_xpath('//*[@id="searchField"]'):
            driver.refresh()
            time.sleep(300)
            driver.refresh()
            time.sleep(200)
            driver.refresh()
            time.sleep(100)
            
            
        search = driver.find_element_by_xpath('//*[@id="searchField"]')
        search.clear()
        search.send_keys(n)
        
        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search_container"]/form/a'))).click()
        #time.sleep()
        
        ### Refines search- selecting only actors
        try:
            WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="NAME"]'))).click()
        except:
            WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="NAME"]'))).click()
        
        try:
            WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="profession"]/ul/li[4]/label'))).click()
        except:
            WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="profession"]/ul/li[4]/label'))).click()
        
        time.sleep(2)

        try:
            ###clicks on first result
            numb = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="results"]/ul/li[1]/ul/li[1]/span/a'))).click()
            if numb == '0':
                f.write('\n'+str(y+1)+'\t')
                f.write(str(n)+'\t')
                f.write(str(star_w.get(y))+'\t'+str(oscars_w.get(y))+'\t'+str(another_Wins_w.get(y))+'\t'+str(nominations_w.get(y))+'\t'+str(bignominations_w.get(y)))
                k.write('\n'+str(n))
                y=y+1
                continue
            else:
                WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="results"]/ul/li[1]/ul/li[1]/span/a'))).click()
                rank = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="meter"]/span[1]/span[2]'))).text
                star_w[y] = rank
                
                if driver.find_element_by_xpath('//*[@id="main_details"]/div/div[1]/dl[1]/dd[2]'):
                    ###selects main details header where we have all info abt awards
                    head = driver.find_element_by_xpath('//*[@id="main_details"]/div/div[1]/dl[1]/dd[2]').text
                    new = head.split()
                    ###Sparsing data into required dictionary
                    for i in range(len(new)):
                        try:
                            if new[i] == 'Oscars.':
                                if not new[i-2] == 'for':
                                    oscars_w[y]=new[i-1]
                            elif new[i] == 'Oscar.':
                                if not new[i-2] == 'for':
                                    oscars_w[y] = new[i-1]
                            elif new[i] == 'wins':
                                
                                another_Wins_w[y] = new[i-1]
                            elif new[i] == 'win':
                                another_Wins_w[y] = new[i-1]
                            elif new[i] == 'nominations':
                                nominations_w[y] = new[i-1]
                            elif new[i] == 'nomination':
                                nominations_w[y] = new[i-1]
                            elif new[i] == 'for':
                                bignominations_w[y] = new[i+1]
                                
                        except:
                           print('Exception')

                    f.write('\n'+str(y+1)+'\t')
                    f.write(str(n)+'\t')
                    f.write(str(star_w.get(y))+'\t'+str(oscars_w.get(y))+'\t'+str(another_Wins_w.get(y))+'\t'+str(nominations_w.get(y))+'\t'+str(bignominations_w.get(y)))
                    k.write('\n'+str(n))
                    y=y+1
                
                else:
                    f.write('\n'+str(y+1)+'\t')
                    f.write(str(n)+'\t')
                    f.write(str(star_w.get(y))+'\t'+str(oscars_w.get(y))+'\t'+str(another_Wins_w.get(y))+'\t'+str(nominations_w.get(y))+'\t'+str(bignominations_w.get(y)))
                    k.write('\n'+str(n))
                    y=y+1
                    continue
                    
                
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            f.write('\n'+str(y+1)+'\t')
            f.write(str(n)+'\t')
            f.write(str(star_w.get(y))+'\t'+str(oscars_w.get(y))+'\t'+str(another_Wins_w.get(y))+'\t'+str(nominations_w.get(y))+'\t'+str(bignominations_w.get(y)))
            k.write('\n'+str(n))
            y=y+1
            continue

     
    f.close()    
    name_w_df = pd.DataFrame([name_w]) 
    name_w_df = name_w_df.transpose()       
    rank_w_df = pd.DataFrame([star_w])
    rank_w_df = rank_w_df.transpose()
    oscars_w_df = pd.DataFrame([oscars_w])
    oscars_w_df = oscars_w_df.transpose()
    another_Wins_w_df = pd.DataFrame([another_Wins_w])
    another_Wins_w_df = another_Wins_w_df.transpose()
    nominations_w_df = pd.DataFrame([nominations_w])
    nominations_w_df = nominations_w_df.transpose()
    bignominations_w_df = pd.DataFrame([bignominations_w])
    bignominations_w_df = bignominations_w_df.transpose()
    
    return name_w_df ,rank_w_df, oscars_w_df, nominations_w_df, another_Wins_w_df, bignominations_w_df

##function to get actors list
def actorslist(actors):
    first = actors.loc[:,'actor1'].to_dict()
    second = actors.loc[:,'actor2'].to_dict()
    third = actors.loc[:,'actor3'].to_dict()
    fourth = actors.loc[:,'actor4'].to_dict()
    fifth = actors.loc[:,'actor5'].to_dict()
    
    final = {}
    
    x = 0
    for i in first.values():
        final[x] = i
        x = x+1
        
    for i in second.values():
        final[x] = i
        x=x+1
        
    for i in third.values():
        final[x] = i
        x=x+1
        
    for i in fourth.values():
        final[x] = i
        x=x+1
        
    for i in fifth.values():
        final[x] = i
        x=x+1
    
    action = set(final.values())
    act_list= list(action)
    
    with open('test_actorlist.txt','a+') as f:
        for i in act_list:
            f.write(str(i)+'\n')
            
    return act_list
    



    
    
###function to get actors rank and awards
def actorstarmeter(act_list):
    
    #creating dictionaries
    name = {}
    star = {}
    oscars = {}
    another_Wins = {}
    nominations = {}
    bignominations = {}
    
    start = 0
    
    if os.path.exists('test_actor_list.txt'): 
        with open('test_actor_list.txt','r') as ko: 
            actlist = ko.readlines()
            actlist = set(actlist)
            actlist = list(actlist)
            
        k=open('test_actor_list.txt','a+')
    else:
        k=open('test_actor_list.txt','a+')
    
    if os.path.exists('test_actor.txt'): 
        with open('test_actor.txt','r') as fo: 
            start = len(fo.readlines())
            f=open('test_actor.txt','a+')
    else:
        f=open('test_actor.txt','a+')

    
    driver.get('http://www.imdb.com/')
    
    #searches for login button
    imdbPro = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="navProMenu"]/p/a/img')))
    imdbPro.click()
    
    #clicks on imdblogin
    loginButton = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header_message"]/a')))
    loginButton.click()
    
    login = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_with_imdb_expender"]')))
    login.click()
    
    ###entering login details
    driver.find_element_by_xpath('//*[@id="ap_email"]').send_keys('munna.saisanthosh@gmail.com')
    driver.find_element_by_xpath('//*[@id="ap_password"]').send_keys('Stevens_123')
    WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="signInSubmit"]'))).click()
    

    
    y=start
   
    #passing movie into loop 
    at = []
    for i in actlist:
        at.append(str(i).strip())
        
    for n in act_list[20000: 27000]:
        n = str(n).strip()
        if n in at:
            continue
        
        
        name[y] = n
        print(y+1)
        
        oscars[y] = 0
        another_Wins[y] = 0
        nominations[y] = 0
        bignominations[y] = 0
        
        if not driver.find_element_by_xpath('//*[@id="searchField"]'):
            driver.refresh()
            time.sleep(300)
            driver.refresh()
            time.sleep(200)
            driver.refresh()
            time.sleep(100)
                
            ####passing movie name
        search = driver.find_element_by_xpath('//*[@id="searchField"]')
        search.clear()
        search.send_keys(n)
        
        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search_container"]/form/a'))).click()
        #time.sleep(10)
        
        ### Refines search- selecting only actors
        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="NAME"]'))).click()
        #WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="type"]/ul/li[1]/label'))).click()
        
        time.sleep(2)
        
    
        try:
            ###clicks on first result
            numb = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="title"]/div[1]/div/span/span[1]'))).text
            
            if numb == '0':
                f.write(str(y)+'\t')
                f.write(str(n)+'\t')
                f.write(star.get(y)+ '\t'+oscars.get(y)+'\t'+str(another_Wins.get(y))+'\t'+str(nominations.get(y))+'\t'+str(bignominations.get(y))+'\n')
                k.write(str(n)+'\n')
                y=y+1
                continue
            
            else:
                WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="results"]/ul/li[1]/ul/li[1]/span/a'))).click()
                rank = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="meter"]/span[1]/span[2]'))).text
                star[y] = rank

                if driver.find_element_by_xpath('//*[@id="main_details"]/div/div[1]/dl[1]/dd[2]'):
                        ###selects main details header where we have all info abt awards
                    head = driver.find_element_by_xpath('//*[@id="main_details"]/div/div[1]/dl[1]/dd[2]').text
                    new = head.split()
                   
                    ###Sparsing data into required dictionary
                    for i in range(len(new)):
                        if new[i] == 'Oscars.':
                            if not new[i-2] == 'for':
                                oscars[y]=new[i-1]
                           
                        elif new[i] == 'Oscar.':
                            if not new[i-2] == 'for':
                                oscars[y] = new[i-1]
                        
                        elif new[i] == 'wins':
                            another_Wins[y] = new[i-1]
                        elif new[i] == 'win':
                            another_Wins[y] = new[i-1]
                          
                        elif new[i] == 'nominations':
                            nominations[y] = new[i-1]
                        elif new[i] == 'nomination':
                            nominations[y] = new[i-1]
                                
                        elif new[i] == 'for':
                            bignominations[y] = new[i+1]

                                    
                    f.write(str(y)+'\t')
                    f.write(str(n)+'\t')
                    f.write(star.get(y)+ '\t'+oscars.get(y)+'\t'+str(another_Wins.get(y))+'\t'+str(nominations.get(y))+'\t'+str(bignominations.get(y))+'\n')
                    k.write(str(n)+'\n')
                    y=y+1
                    
                else:
                    f.write(str(y)+'\t')
                    f.write(str(n)+'\t')
                    f.write(star.get(y)+ '\t'+oscars.get(y)+'\t'+str(another_Wins.get(y))+'\t'+str(nominations.get(y))+'\t'+str(bignominations.get(y))+'\n')
                    k.write(str(n)+'\n')
                    y=y+1
                        
        
            
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            print('Exception')
            continue

    k.close()
    f.close()
    
    name = pd.DataFrame([name])  
    name = name.transpose()     
    rank = pd.DataFrame([star])
    rank = rank.transpose() 
    oscars = pd.DataFrame([oscars])
    oscars = oscars.transpose() 
    another_Wins = pd.DataFrame([another_Wins])
    another_Wins = another_Wins.transpose() 
    nominations = pd.DataFrame([nominations])
    nominations= nominations.transpose() 
    bignominations = pd.DataFrame([bignominations])
    bignominations = bignominations.transpose() 
     
    return name, rank, oscars, nominations, another_Wins, bignominations  

    
###merging actors to their original formats


if __name__ == "__main__":
    imdb_new = pd.read_csv('imdb_awd.csv',encoding='utf-8')
    imdb_new.replace(r'\s+', np.nan, regex=True)
    
    #Web Driver
    ua=UserAgent()
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (ua.random)
    service_args=['--ssl-protocol=any','--ignore-ssl-errors=true']
    driver = webdriver.Chrome(desired_capabilities=dcap,service_args=service_args)
    
    ####Run 2nd- scrapes actor information from imdb and writes into out_actor.csv file. When program stops run file again
    
    ###if program stops after 1st time comment below two lines and run file again
    act_list = actorslist(imdb_new)
    name_a, rank_a, oscars_a, nominations_a, another_wins_a, bignominations_a = actorstarmeter(act_list)
    
    
    actor_final = pd.concat([name_a, rank_a, oscars_a, nominations_a, another_wins_a, bignominations_a],axis=1)
    actor_final.columns = ['name_a', 'rank_a', 'oscars_a', 'nominations_a', 'another_wins_a', 'bignominations_a']
    
    
    if os.path.exists('out_actor.csv'): 
        with open('out_actor.csv', 'a+') as act:
            actor_final.to_csv(act, header=False, na_rep = np.nan, encoding='utf-8')
    else:
        with open('out_actor.csv', 'a+') as act:
            actor_final.to_csv(act, header=True, na_rep = np.nan, encoding='utf-8')
    
    ###Run 3rd- scrapes writers information from imdb into out_writer.csv file. Run file if program stops
    ###if program stops after 1st time comment below two lines and run file again
    writer_list = writerslist(imdb_new)
    name_w, rank_w, oscars_w, nominations_w, another_wins_w, bignominations_w  = writerstarmeter(writer_list)
    
    
    writer_final = pd.concat([name_w, rank_w, oscars_w, nominations_w, another_wins_w, bignominations_w],axis=1)
    writer_final.columns = ['name_w', 'rank_w', 'oscars_w', 'nominations_w', 'another_wins_w', 'bignominations_w']
    
    
    if os.path.exists('out_writer.csv'): 
        with open('out_writer.csv', 'a+') as act:
            writer_final.to_csv(act, header=False, na_rep = np.nan, encoding='utf-8')
    else:
        with open('out_writer.csv', 'a+') as act:
            writer_final.to_csv(act, header=True, na_rep = np.nan, encoding='utf-8')

    ###Run 4th- scrapes directors information from imdb into out_director.csv file. Run file if program stops.
    
    ###if program stops after 1st time comment below two lines and run file again
    direct_list = directorslist(imdb_new)
    name_d, rank_d, oscars_d, nominations_d, another_wins_d, bignominations_d = directorstarmeter(direct_list)
    
    director_final = pd.concat([name_d, rank_d, oscars_d, nominations_d, another_wins_d, bignominations_d],axis=1)
    director_final.columns = ['name_d', 'rank_d', 'oscars_d', 'nominations_d', 'another_wins_d', 'bignominations_d']
    
    
    if os.path.exists('out_director.csv'): 
        with open('out_director.csv', 'a+') as act:
            director_final.to_csv(act, header=False, na_rep = np.nan, encoding='utf-8')
    else:
        with open('out_director.csv', 'a+') as act:
            writer_final.to_csv(act, header=True, na_rep = np.nan, encoding='utf-8')

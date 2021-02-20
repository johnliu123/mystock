#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 09:22:26 2021

@author: johnliu
"""



import requests
from bs4 import BeautifulSoup
import re
#from fake_useragent import UserAgent
import pandas as pd
import numpy as np


def Eps_crab(industry_new):
    
    
    # 要抓取的網址
    url = 'https://goodinfo.tw/StockInfo/StockList.asp?MARKET_CAT=全部&INDUSTRY_CAT='+industry_new+'&SHEET=年獲利能力_近N年一覽&SHEET2=EPS年成長率(%25)&RPT_TIME=最新資料'
    #user_agent = UserAgent()
    
    headers = {
        "Authorization": "Bearer " + "YkrXjA4k7pswPML2wkdNxgcRhqSKPcrBysvLmIClsvd",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "zh-TW,zh;q=0.9", 
        #"Host": "goodinfo.tw/StockInfo/index.asp",  #目標網站 
        "Sec-Fetch-Dest": "document", 
        "Sec-Fetch-Mode": "navigate", 
        "Sec-Fetch-Site": "none", 
        "Upgrade-Insecure-Requests": "1", 
        #隨機設定 使用者代理(User-Agent)
        #"User-Agent":user_agent.random,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36", #使用者代理
        "Referer": "https://www.google.com/"
        
    }
    
    
    
    #請求網站
    list_req = requests.post(url, headers = headers)
    
    #result=str(list_req)
    #return result
    
    #將整個網站的程式碼爬下來
    soup = BeautifulSoup(list_req.content, "html.parser")
    
    stockEps=soup.find_all(id=re.compile('^row'))

    #取出股票代號及EPS結果
    
    stock_num_list=[]
    stock_Eps_list=[]
    
    for Eps in range(0,len(stockEps)):
        stocknum=stockEps[Eps].find_all('nobr')[0].text
        resultEPS=stockEps[Eps].find_all('nobr')[-1].text
        stock_num_list.append(stocknum)
        stock_Eps_list.append(resultEPS)
    
    
    
    #欄位合併
    stockresult_list={"代號":stock_num_list,"EPS年成長率(%)":stock_Eps_list}
    df_stock=pd.DataFrame(stockresult_list)
    
    
    df_stock=df_stock[df_stock['EPS年成長率(%)'].str.contains("\+")]
    
    
    df_stock_num_result=df_stock["代號"].tolist()
    
    
    result_stock=""
    
    for i in df_stock_num_result:
        url1='http://jsjustweb.jihsun.com.tw/z/zc/zca/zca_'+i+'.djhtm'
        #請求網站
        list_req1 = requests.post(url1, headers = headers)
        #將整個網站的程式碼爬下來
        soup1 = BeautifulSoup(list_req1.content, "html.parser")
        td=soup1.find_all('td')[4]
        a=td.text
        a=a.lstrip()
        a=a.split(" ")
        a=a[0]
        a=a.split("(")
        a=a[0]
        a=a.replace("*","")
        #print(i+a+' ')
        result=i+a+' '
        result_stock+=result+'\n'
        #print(result_stock)
        #result_stock_list.append(result)
    #print(industry_new+'相關類股其今年累計EPS年度成長率優於去年者，適合購買的股票為:'+'\n'+result_stock)
    
    result=industry_new+'相關類股其今年累計EPS年度成長率優於去年者，適合購買的股票為:'+'\n'+result_stock
    
    
    
    params = {"message": industry_new+'相關類股其今年累計EPS年度成長率優於去年者，適合購買的股票為:'+'\n'+result_stock}
    r = requests.post("https://notify-api.line.me/api/notify",
                                              headers=headers, params=params)

    
    
    
    
    return result
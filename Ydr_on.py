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
import stockmd


def Ydr_crab(industry_new):
    
    
    # 要抓取的網址
    url = 'https://goodinfo.tw/StockInfo/StockList.asp?MARKET_CAT=全部&INDUSTRY_CAT='+industry_new+'&SHEET=股利政策發放年度_近N年股利一覽&SHEET2=現金%2B股票年均殖利率&RPT_TIME=最新資料'
    
    
    """
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
    """
    
    headers=stockmd.get_headers()
    
    #請求網站
    list_req = requests.post(url, headers = headers)
    
    #result=str(list_req)
    #return result
    
    #將整個網站的程式碼爬下來
    soup = BeautifulSoup(list_req.content, "html.parser")
    
    stock_result=soup.find_all("a", { "class" : "link_black","style":"cursor:pointer;"})


    #取出近5年Yieldrate欄位名稱
    stock_name_list=[]
    for i in range(0,22):
        name=stock_result[i].text
        if i >=16:
            stock_name_list.append(name)
            
    
    stockYdr=soup.find_all(id=re.compile('^row'))
    
    stock_num_list=[]
    #計算倒數前6個table
    stockYdr_reciprocal1_table=[]
    stockYdr_reciprocal2_table=[]
    stockYdr_reciprocal3_table=[]
    stockYdr_reciprocal4_table=[]
    stockYdr_reciprocal5_table=[]
    stockYdr_reciprocal6_table=[]
    stockYdrYr_list=[stockYdr_reciprocal1_table,stockYdr_reciprocal2_table,stockYdr_reciprocal3_table,stockYdr_reciprocal4_table,stockYdr_reciprocal5_table,stockYdr_reciprocal6_table]
    
    
    
    
    
    #取出近5年的Yieldrate數值
    table=-1
    for stocklist in stockYdrYr_list:
        for num in range(0,len(stockYdr)):
            result=stockYdr[num].find_all('nobr')[table].text
            stocklist.append(result)
        table=table-1
    
    
    #取出代號
    for num in range(0,len(stockYdr)):
        result=stockYdr[num].find_all('nobr')[0].text
        stock_num_list.append(result)
    
    
    
    
    #欄位合併
    stockresult_list={"代號":stock_num_list,stock_name_list[0]:stockYdr_reciprocal6_table,stock_name_list[1]:stockYdr_reciprocal5_table,stock_name_list[2]:stockYdr_reciprocal4_table
                     ,stock_name_list[3]:stockYdr_reciprocal3_table,stock_name_list[4]:stockYdr_reciprocal2_table
                     ,stock_name_list[5]:stockYdr_reciprocal1_table}
    df_stock=pd.DataFrame(stockresult_list)
    
    
    
    #去除空白
    df_stock = df_stock.replace(r'^\s*$', np.nan, regex=True)
    
    
    #判斷第5行欄位空值數量 只取5年的Yieldrate
    isnanum=df_stock[df_stock.columns[6]].isna().sum()
    if isnanum>10:
        df_stock=df_stock.drop([df_stock.columns[6]],axis=1)
    else:
        df_stock=df_stock.drop([df_stock.columns[1]],axis=1)
        
    
    for i in df_stock.iloc[:,1:]:
        df_stock[i]=df_stock[i].astype(str).astype(float)
        
        
    
    df_stock_result=df_stock.loc[(df_stock[df_stock.columns[1]]>=5)&(df_stock[df_stock.columns[2]]>=5)&(df_stock[df_stock.columns[3]]>=5)&(df_stock[df_stock.columns[4]]>=5)&(df_stock[df_stock.columns[5]]>=5)]
                                
    
    df_stock_num_result=df_stock_result["代號"].tolist()
    
    result_stock=stockmd.stock_result(headers,df_stock_num_result)
    
    """
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
        url2='https://tw.stock.yahoo.com/q/q?s='+i
        #請求網站
        list_req2 = requests.post(url2, headers = headers)
        #將整個網站的程式碼爬下來
        soup2 = BeautifulSoup(list_req2.content, "html.parser")
        b=soup2.find_all('td')[5].text
        result=i+a+' '+'目前價格:'+b+'元'
        result_stock+=result+'\n'
        #print(result_stock)
        #result_stock_list.append(result)
    
    """
    
    #print(industry_new+'相關類股其近五年Ydr>=5，適合購買的股票為:'+'\n'+result_stock)
    
    
    result='相關類股其近五年Ydr>=5，適合購買的股票為:'+'\n'+result_stock
    
    
    #params = {"message": industry_new+'相關類股其近五年Ydr>=5，適合購買的股票為:'+'\n'+result_stock}
    #r = requests.post("https://notify-api.line.me/api/notify",
                                              #headers=headers, params=params)
    
    return result
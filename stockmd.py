#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 23:19:42 2021

@author: johnliu
"""

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_headers():
    
    user_agent = UserAgent()
    
    token='YkrXjA4k7pswPML2wkdNxgcRhqSKPcrBysvLmIClsvd' 
    
    headers = {
        
        "Authorization": "Bearer " + token,
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

    return headers


def stock_result(headers,stock):
    
    result_stock=''
    
    for number in stock:
       url_stock_name='http://jsjustweb.jihsun.com.tw/z/zc/zca/zca_'+number+'.djhtm'
       #請求網站
       list_req_stock_name = requests.post(url_stock_name, headers = headers)
       #將整個網站的程式碼爬下來
       soup_req_stock_name = BeautifulSoup(list_req_stock_name.content, "html.parser")
       td=soup_req_stock_name.find_all('td')[4]
       name=td.text
       name=name.lstrip()
       name=name.split(" ")
       name=name[0]
       name=name.split("(")
       name=name[0]
       name=name.replace("*","")
       #print(i+a+' ')
       url_stock_price='https://tw.stock.yahoo.com/q/q?s='+number
       #請求網站
       list_req_stock_price = requests.post(url_stock_price, headers = headers)
       #將整個網站的程式碼爬下來
       soup_stock_price = BeautifulSoup(list_req_stock_price.content, "html.parser")
       price=soup_stock_price.find_all('td')[5].text
       result=number+name+' '+'目前價格:'+price+'元'
       result_stock+=result+'\n'
    return result_stock
   
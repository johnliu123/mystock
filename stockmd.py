#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 23:19:42 2021

@author: johnliu
"""

import requests
from bs4 import BeautifulSoup


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
   
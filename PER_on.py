#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 09:22:26 2021

@author: johnliu
"""

"""
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import mongodb

from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackAction,
    CarouselColumn,
    CarouselTemplate,
    PostbackTemplateAction
)



"""

import requests
from bs4 import BeautifulSoup
import re
#from fake_useragent import UserAgent

import numpy as np


def PER_crab(industry_new):
    
    
    # 要抓取的網址
    url = 'https://goodinfo.tw/StockInfo/StockList.asp?MARKET_CAT=全部&INDUSTRY_CAT='+industry_new+'&SHEET=交易狀況&SHEET2=日&RPT_TIME=最新資料'
    
    
    user_agent = UserAgent()
    
    headers = {
            
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
    
    
    #取text數字(股票代碼) 先存成list 再用迴圈取出來
    stock_mun=soup.find_all(class_="link_black",target="_blank",text=re.compile('\d{4}'),href=re.compile("StockDetail"))
    
    
    
    stock_mun_list=[]
    
    for num in stock_mun:
        #print(num.text)
        stock_mun_list.append(num.text)
        #result=str(num.text)
        
    
    
    #去除重複的股票代碼
    stock_mun_list=np.unique(stock_mun_list).tolist()
    
    
    
    stock1=[]

    for num in stock_mun_list:
        #print(num)
        try:
            url1='http://jsjustweb.jihsun.com.tw/z/zc/zca/zca_'+num+'.djhtm'
            #請求網站
            list_req1 = requests.post(url1, headers = headers)
            #將整個網站的程式碼爬下來
            soup1 = BeautifulSoup(list_req1.text, "html.parser")
            tr=soup1.find_all('tr')[6]
            td=tr.find_all('td')[1]
            PBR= td.text
            PBR=PBR.replace(",", "")
            if PBR =='N/A':
                #print("空值")
                pass
                #continue
                #break
            else:
                tr1=soup1.find_all('tr')[7]
                td1=tr1.find_all('td')[1]
                avrPBR= td1.text
                PBR=float(PBR)
                avrPBR=avrPBR.replace(",", "")
                avrPBR=float(avrPBR)
                
                if PBR<=15:
                    
                    if PBR<avrPBR:
                        #print('本益比小')
                        stock1.append(num)
                    else:
                        #print('本益比大')
                        pass
                else:
                    #print('本益比大')
                    pass
        except IndexError:
                pass
    
    
    
    #result_stock_list=[]
    result_stock=''
    
    for i in stock1:
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
        
    
    result='相關類股其本益比<=15適合購買的股票為:'+'\n'+result_stock
    #params = {"message": '半導體業相關類股其本益比較小適合購買的股票為:'+'\n'+result_stock}
    #r = requests.post("https://notify-api.line.me/api/notify",
                                              #headers=headers2, params=params)
    
    return result
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 13:41:10 2019

@author: aaaaa
"""

from __future__ import print_function
import time
from linebot import (LineBotApi, WebhookHandler, exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import schedule
from pymongo import MongoClient
import urllib.parse
import datetime
import requests
from bs4 import BeautifulSoup
import mongodb

import random
from fake_useragent import UserAgent


#line message api 設定
# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('ps8rdB2odqUku93oarX0pEY5N2KiN5Fbw5pWQ5rPBR9IPAm0IpM+Y9xLTB2wyiTsUQyRzrnGyvnIiK0cymhJQjNmrOVLEfOlQyEfE1DYryo5b6aYPrjm10aLYeb9R/z1RP+yGj6jQ0fTLdtGWDgK0wdB04t89/1O/w1cDnyilFU=')
yourid='U0db823667b9edd2dfea67e380d87cf41'

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
    "User-Agent":user_agent.random,
    #"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36" #使用者代理
    "Referer": "https://www.google.com/"
}

def job():
    
    data = mongodb.show_user_stock_fountion()
    
    for i in data:
        stock=i['stock']
        bs=i['bs']
        price=i['price']
        
        #yahoo的 要使用list_req.text 
        url = 'https://tw.stock.yahoo.com/q/q?s=' + stock 
        list_req = requests.get(url, headers = headers)
        
        try:
            #要使用try catch 不然爬蟲更新價格時有時還沒有更新會抓不到資料會有error
            #要使用list_req.text 不是使用list_req.content不然會有亂碼
            soup = BeautifulSoup(list_req.text, "html.parser")
            tables=soup.find_all('table')[1] #裡面所有文字內容
            table1=soup.find_all('table')[2]
            a=table1.find_all("a")[0].text[4:]#股票名稱
            tds=tables.find_all("td")[3]
            getstock= tds.find('b').text
        
            if float(getstock):
                if bs == '<':
                    if float(getstock) < price:
                        get=stock+a+ ' 的價格：'+str(getstock)+' 已低於您設定的價格'+str(price)+'元，'+'即可買入！！'
                        #line_bot_api.push_message(yourid, TextSendMessage(text=get))
                        print(get)
                else:
                    if float(getstock) > price:
                        
                        get=stock+a+ ' 的價格：'+str(getstock)+' 已高於您設定的價格'+str(price)+'元，'+'即可賣出！！'
                        #line_bot_api.push_message(yourid, TextSendMessage(text=get))
                        print(get)
            else:
                #line_bot_api.push_message(yourid, TextSendMessage(text='這個有問題'))
                print("有問題")
        
        except IndexError:
            pass
        
        

schedule.every(10).seconds.do(job) #每10秒執行一次

# 無窮迴圈
while True: 
    schedule.run_pending()
    #設定隨機的延遲時間 避免相同的request時間
    delay_choices = [8, 5, 10, 6, 20, 11]  #延遲的秒數
    #delay_choices = [1,2,3]  #延遲的秒數
    delay = random.choice(delay_choices)  #隨機選取秒數
    time.sleep(delay)  #延遲

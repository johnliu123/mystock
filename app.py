#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import mongodb
import re
import requests
from bs4 import BeautifulSoup

def stock_Strategy(usespeakStrategy):
    line_bot_api.push_message(uid,TextSendMessage("測試成功"))


app = Flask(__name__)

#line message api 設定
# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('ps8rdB2odqUku93oarX0pEY5N2KiN5Fbw5pWQ5rPBR9IPAm0IpM+Y9xLTB2wyiTsUQyRzrnGyvnIiK0cymhJQjNmrOVLEfOlQyEfE1DYryo5b6aYPrjm10aLYeb9R/z1RP+yGj6jQ0fTLdtGWDgK0wdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('1c771de5f787f511840d0f1402d12b47')

#開始啟用時的預設對話
line_bot_api.push_message('U0db823667b9edd2dfea67e380d87cf41', TextSendMessage(text='歡迎使用股市小助手！！'))

# 監聽所有來自 /callback 的 Post Request
#接收line的回傳資訊
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
#reply_message 使用者輸入訊息 line會回覆相同訊息 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #取得顧客資訊
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id #使用者ID
    usespeak=str(event.message.text) #使用者講的話
    if re.match('[0-9]{4}[<>][0-9]',usespeak): # 先判斷是否是使用者要用來存股票的
        mongodb.write_user_stock_fountion(stock=usespeak[0:4], bs=usespeak[4:5], price=usespeak[5:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak[0:4]+'已經儲存成功'))
        return 0

    
    elif re.match('刪除[0-9]{4}',usespeak): # 刪除存在資料庫裡面的股票
        mongodb.delete_user_stock_fountion(stock=usespeak[2:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak+'已經刪除成功'))
        return 0
    
    
    elif re.match('[0-9]{4}價格',usespeak): # 先判斷是否是使用者要用來存股票的
        
        data = mongodb.show_user_stock_fountion()

        stock_price=[]
        
        for i in data:
              stock=i['stock']
              bs=i['bs']
              price=i['price']
              stock_price.append(stock)
              
        if usespeak[0:4] in stock_price:              
            url = 'https://tw.stock.yahoo.com/q/q?s=' + usespeak[0:4] 
            list_req = requests.get(url)
            soup = BeautifulSoup(list_req.text, "html.parser")
            tables=soup.find_all('table')[1] #裡面所有文字內容
            table1=soup.find_all('table')[2]
            a=table1.find_all("a")[0].text[4:]#股票名稱
            tds=tables.find_all("td")[3]
            getstock= tds.find('b').text
            getstock=float(getstock)
            get=str(usespeak[0:4])+a+' 的價格：' + str(getstock)
            line_bot_api.push_message(uid, TextSendMessage(get))

               
        else:
            #print("查無此股票價格！！")
            line_bot_api.push_message(uid,TextSendMessage(usespeak[0:4]+"查無此股票價格！！"))
              
        return 0
    
    
    elif re.match('買股票',usespeak): # 刪除存在資料庫裡面的股票
        line_bot_api.push_message(uid,TextSendMessage("請輸入你要的選股策略:"))
        usespeakStrategy=str(event.message.text) #使用者講的話
        if re.match('測試',usespeakStrategy): # 刪除存在資料庫裡面的股票
            #line_bot_api.push_message(uid,TextSendMessage("測試"))
            line_bot_api.reply_message(event.reply_token,"測試")
            #stock_Strategy(usespeakStrategy)
        
        
        return 0
    
    
    """
    elif re.match('[0-9]{4}價格',usespeak): # 先判斷是否是使用者要用來存股票的
        
        data=mongodb.show_user_stock_fountion()
        
        for i in data:
           stock=i['stock']
           bs=i['bs']
           price=i['price']
                
           url = 'https://tw.stock.yahoo.com/q/q?s=' + stock 
           list_req = requests.get(url)
           soup = BeautifulSoup(list_req.content, "html.parser")
           tables=soup.find_all('table')[1] #裡面所有文字內容
           tds=tables.find_all("td")[3]
           getstock= tds.find('b').text
           getstock=float(getstock)
        
           if getstock< price:
              get=str(stock) + '的價格：' + str(getstock)
              #print(get)
              line_bot_api.push_message(uid, TextSendMessage(get+"結果"))
              
           else:
              get=str(stock) + '的價格：' + str(getstock)
              #print(get)
              line_bot_api.push_message(uid,TextSendMessage(get+"結果"))
              
        return 0
        
        """        
        
"""
@handler.add(MessageEvent, message=TextMessage)
def handle_message1(event):
    #取得顧客資訊
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id #使用者ID
    usespeak=str(event.message.text) #使用者講的話
    
    if re.match('[0-9]{4}價格',usespeak): # 先判斷是否是使用者要用來存股票的
        
        data = mongodb.show_user_stock_fountion()

        stock_price=[]
        
        for i in data:
              stock=i['stock']
              bs=i['bs']
              price=i['price']
              stock_price.append(stock)
              
        if usespeak[0:4] in stock_price:              
            url = 'https://tw.stock.yahoo.com/q/q?s=' + usespeak[0:4] 
            list_req = requests.get(url)
            soup = BeautifulSoup(list_req.content, "html.parser")
            tables=soup.find_all('table')[1] #裡面所有文字內容
            tds=tables.find_all("td")[3]
            getstock= tds.find('b').text
            getstock=float(getstock)
            get=str(usespeak[0:4]) + '的價格：' + str(getstock)
            line_bot_api.push_message(uid, TextSendMessage(get))

               
        else:
            #print("查無此股票價格！！")
            line_bot_api.push_message(uid,TextSendMessage(usespeak[0:4]+"查無此股票價格！！"))
              
        return 0
    
"""  

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run(debug=True)

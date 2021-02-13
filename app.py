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
import PER_on
import re
import requests
from bs4 import BeautifulSoup


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
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    "Referer": "https://www.google.com/"
}




#global 定義全域變數 交換變數
def save_industry(industry):
    global industry_new
    if industry !="":
        industry_new=industry
        return industry_new
    else:
        return industry_new
    


def stock_propose_template():
    
    stock_project_template=TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='請輸入你要的選股策略:',
                                text='請選擇選股標的',
                                actions=[
                                    PostbackAction(
                                        label='1.本益比',
                                        text='1.本益比',
                                        data='本益比'
                                    ),
                                    PostbackAction(
                                        label='2.殖利率',
                                        text='2.殖利率',
                                        data='殖利率'
                                    ),
                                    PostbackAction(
                                        label='3.EPS',
                                        text='3.EPS',
                                        data='EPS'
                                    )
                                ]
                            )
                        )
    
    return stock_project_template
    

def stock_template():
    
    Carousel_template = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
        columns=[
            CarouselColumn(
                title='請輸入類股代號：',
                text='請選擇產業類股',
                actions=[
                    PostbackAction(
                            label='1.水泥工業',
                            text='1.水泥工業',
                            data='水泥工業'
                            ),
                    PostbackAction(
                            label='2.食品工業',
                            text='2.食品工業',
                            data='食品工業'
                            ),
                    PostbackAction(
                            label='3.塑膠工業',
                            text='3.塑膠工業',
                            data='塑膠工業'
                            ),
                    
                ]
            ),
            CarouselColumn(
                title='請輸入類股代號：',
                text='請選擇產業類股',
                actions=[
                    PostbackAction(
                            label='4.紡織纖維',
                            text='4.紡織纖維',
                            data='紡織纖維'
                            ),
                    PostbackAction(
                            label='5.電機機械',
                            text='5.電機機械',
                            data='電機機械'
                            ),
                    PostbackAction(
                            label='6.電器電纜',
                            text='6.電器電纜',
                            data='電器電纜'
                            ),
                    
                ]
            ),
            CarouselColumn(
                title='請輸入類股代號：',
                text='請選擇產業類股',
                actions=[
                    PostbackAction(
                            label='7.生技醫療業',
                            text='7.生技醫療業',
                            data='生技醫療業'
                            ),
                    PostbackAction(
                            label='8.化學工業',
                            text='8.化學工業',
                            data='化學工業'
                            ),
                    PostbackAction(
                            label='9.玻璃陶瓷',
                            text='9.玻璃陶瓷',
                            data='玻璃陶瓷'
                            ),
                    
                ]
            ),
            CarouselColumn(
                title='請輸入類股代號：',
                text='請選擇產業類股',
                actions=[
                    PostbackAction(
                            label='10.造紙工業',
                            text='10.造紙工業',
                            data='造紙工業'
                            ),
                    PostbackAction(
                            label='11.鋼鐵工業',
                            text='11.鋼鐵工業',
                            data='鋼鐵工業'
                            ),
                    PostbackAction(
                            label='12.橡膠工業',
                            text='12.橡膠工業',
                            data='橡膠工業'
                            ),
                    
                ]
            ),
            CarouselColumn(
                title='請輸入類股代號：',
                text='請選擇產業類股',
                actions=[
                    PostbackAction(
                            label='13.汽車工業',
                            text='13.汽車工業',
                            data='汽車工業'
                            ),
                    PostbackAction(
                            label='14.電腦及週邊設備業',
                            text='14.電腦及週邊設備業',
                            data='電腦及週邊設備業'
                            ),
                    PostbackAction(
                            label='15.半導體業',
                            text='15.半導體業',
                            data='半導體業'
                            ),
                    
                ]
            ),
            CarouselColumn(
                title='請輸入類股代號：',
                text='請選擇產業類股',
                actions=[
                    PostbackAction(
                            label='16.電子零組件業',
                            text='16.電子零組件業',
                            data='電子零組件業'
                            ),
                    PostbackAction(
                            label='17.其他電子業',
                            text='17.其他電子業',
                            data='其他電子業'
                            ),
                    PostbackAction(
                            label='18.通信網路業',
                            text='18.通信網路業',
                            data='通信網路業'
                            ),
                    
                ]
            ),
            CarouselColumn(
                title='請輸入類股代號：',
                text='請選擇產業類股',
                actions=[
                    PostbackAction(
                            label='19.資訊服務業',
                            text='19.資訊服務業',
                            data='資訊服務業'
                            ),
                    PostbackAction(
                            label='20.建材營造業',
                            text='20.建材營造業',
                            data='建材營造業'
                            ),
                    PostbackAction(
                            label='21.航運業',
                            text='21.航運業',
                            data='航運業'
                            ),
                    
                ]
            ),
            CarouselColumn(
                title='請輸入類股代號：',
                text='請選擇產業類股',
                actions=[
                    PostbackAction(
                            label='22.觀光事業',
                            text='22.觀光事業',
                            data='觀光事業'
                            ),
                    PostbackAction(
                            label='23.銀行業',
                            text='23.銀行業',
                            data='銀行業'
                            ),
                    PostbackAction(
                            label='24.保險業',
                            text='24.保險業',
                            data='保險業'
                            ),
                    
                ]
            ),
            CarouselColumn(
                title='請輸入類股代號：',
                text='請選擇產業類股',
                actions=[
                    PostbackAction(
                            label='25.金控業',
                            text='25.金控業',
                            data='金控業'
                            ),
                    PostbackAction(
                            label='26.貿易百貨業',
                            text='26.貿易百貨業',
                            data='貿易百貨業'
                            ),
                    PostbackAction(
                            label='27.光電業/28.電子通路業',
                            text='27.光電業/28.電子通路業',
                            data='光電業/電子通路業'
                            ),
                    
                ]
            ),
            CarouselColumn(
                title='請輸入類股代號：',
                text='請選擇產業類股',
                actions=[
                    PostbackAction(
                            label='29.證券業/30.其他業',
                            text='29.證券業/30.其他業',
                            data='證券業/其他業'
                            ),
                    PostbackAction(
                            label='31.油電燃氣業/32.電子商務',
                            text='31.油電燃氣業/32.電子商務',
                            data='油電燃氣業/電子商務'
                            ),
                    PostbackAction(
                            label='33.文化創意業/34.農業科技業',
                            text='33.文化創意業/34.農業科技業',
                            data='文化創意業/農業科技業'
                            ),
                    
                ]
            ) 
        ]
    )
    )
    
    return Carousel_template



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
    
    elif re.match('測試',usespeak): # 取得id
        #line_bot_api.push_message(uid,TextSendMessage("你的id"+uid))
        #line_bot_api.push_message(uid,TextSendMessage("測試"))
        #line_bot_api.reply_message(event.reply_token,"測試")
        
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入您的姓名"))
        #line_bot_api.push_message(uid,TextSendMessage("請輸入您的姓名"))
        username=str(event.message.text)
        line_bot_api.reply_message(event.reply_token,"已輸入"+username)
        """
        if re.match('[^0-9]',username):
        #if event.message.text !="":
            
            #line_bot_api.reply_message(uid,"請輸入您的token碼")
            line_bot_api.push_message(uid,TextSendMessage("請輸入您的token碼"))
            usertoken=str(event.message.text)
            if re.match('[^0-9]',usertoken):
            #if event.message.text !="":
                #usertoken=str(event.message.text)
                mongodb.write_user_information_fountion(uid,username,usertoken)
        """
        
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
        #line_bot_api.push_message(uid,TextSendMessage("請輸入你要的選股策略:"))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入你要的選股策略:"))
        #usespeakStrategy=str(event.message.text) #使用者講的話
        
        if uid=="U0db823667b9edd2dfea67e380d87cf41":
            #選擇產業類股
            Carousel_template=stock_template()
            
            line_bot_api.reply_message(event.reply_token,Carousel_template)
            
            
            return 0
        else:
            
            line_bot_api.push_message(uid,TextSendMessage("無權限"))
            return 0
    
    
    
      
@handler.add(PostbackEvent)
def handle_postback(event):
    
    # event.postback.data 取得使用者點選回傳值的結果
    if event.postback.data == '光電業/電子通路業':  
        Carousel_template = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
        columns=[
            CarouselColumn(
                title='請輸入類股代號：',
                text='請選擇產業類股',
                actions=[
                    PostbackAction(
                            label='27.光電業',
                            text='27.光電業',
                            data='光電業'
                            ),
                    PostbackAction(
                            label='28.電子通路業',
                            text='28.電子通路業',
                            data='電子通路業'
                            ),
                ]
            )
        ]
    )
    )
        line_bot_api.reply_message(event.reply_token,Carousel_template)
        
    elif event.postback.data == '證券業/其他業':  
        Carousel_template = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
        columns=[
            CarouselColumn(
                title='請輸入類股代號：',
                text='請選擇產業類股',
                actions=[
                    PostbackAction(
                            label='29.證券業',
                            text='29.證券業',
                            data='證券業'
                            ),
                    PostbackAction(
                            label='30.其他業',
                            text='30.其他業',
                            data='其他業'
                            ),
                ]
            )
        ]
    )
    )
        line_bot_api.reply_message(event.reply_token,Carousel_template)
        
    elif event.postback.data == '油電燃氣業/電子商務':  
        Carousel_template = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
        columns=[
            CarouselColumn(
                title='請輸入類股代號：',
                text='請選擇產業類股',
                actions=[
                    PostbackAction(
                            label='31.油電燃氣業',
                            text='31.油電燃氣業',
                            data='油電燃氣業'
                            ),
                    PostbackAction(
                            label='32.電子商務',
                            text='32.電子商務',
                            data='電子商務'
                            ),
                ]
            )
        ]
    )
    )
        line_bot_api.reply_message(event.reply_token,Carousel_template)
        
    elif event.postback.data == '文化創意業/農業科技業':  
        Carousel_template = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
        columns=[
            CarouselColumn(
                title='請輸入類股代號：',
                text='請選擇產業類股',
                actions=[
                    PostbackAction(
                            label='33.文化創意業',
                            text='33.文化創意業',
                            data='文化創意業'
                            ),
                    PostbackAction(
                            label='34.農業科技業',
                            text='34.農業科技業',
                            data='農業科技業'
                            ),
                ]
            )
        ]
    )
    )
        line_bot_api.reply_message(event.reply_token,Carousel_template)
    
    
    
    elif event.postback.data == '水泥工業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)
                        
                        
    elif event.postback.data == '食品工業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)               
        
    
    elif event.postback.data == '塑膠工業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '紡織纖維':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    
    elif event.postback.data == '電機機械':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '電器電纜':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '生技醫療業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '化學工業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '玻璃陶瓷':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '造紙工業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '鋼鐵工業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '橡膠工業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '汽車工業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '電腦及週邊設備業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '半導體業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '電子零組件業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '其他電子業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '通信網路業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '資訊服務業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '建材營造業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '航運業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '觀光事業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '銀行業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '保險業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)  
    
    elif event.postback.data == '金控業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template) 
    
    elif event.postback.data == '貿易百貨業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template) 
    
    

    elif event.postback.data == '光電業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)
    
    elif event.postback.data == '電子通路業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)
    
    elif event.postback.data == '證券業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)
    
    elif event.postback.data == '其他業':
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)
    
    elif event.postback.data == '油電燃氣業':
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)
        
    elif event.postback.data == '電子商務':
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)
        
    elif event.postback.data == '文化創意業': 
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template)
        
    elif event.postback.data == '農業科技業':  
        
        industry=event.postback.data
        
        save_industry(industry)
        
        stock_project_template=stock_propose_template()
        
        # 回復傳入的訊息文字
        line_bot_api.reply_message(event.reply_token,stock_project_template) 
        
       
    
    
    # event.postback.data 取得使用者點選回傳值的結果
    elif event.postback.data == '本益比':
        
        
        industry_new=save_industry(industry="")
        
        result=PER_on.PER_crab(industry_new)
        
        
        params = {"message":industry_new+result}
        r = requests.post("https://notify-api.line.me/api/notify",
                                          headers=headers, params=params)
        
    
    elif event.postback.data == '殖利率':
        result = event.postback.data
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您選擇的是"+result))
    
    
    elif event.postback.data == 'EPS':  
        result = event.postback.data
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您選擇的是"+result))

     



#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run(debug=True)

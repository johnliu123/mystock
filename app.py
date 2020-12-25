#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

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
    profile=line_bot_api.get_profile(event.source.user_id)
    uid=profile.user_id
    usespeak=str(event.message.test)
    if re.match('[0-9]{4}[<>][0-9]',usespeak):
        mongodb.write_user_stock(stock=usespeak[0:4],bs=usespeak[4:5],price=usespeak[5:])
        line_bot_api.push_message(uid,TextSendMessage(usespeak[0:4]+'已經儲存成功'))
        return
    
    elif re.match('刪除[0-9]{4}',usespeak):
        mongodb.delete_user_stock(stock=usespeak[2:])
        line_bot_api.push_message(uid,TextSendMessage(usespeak+'已經刪除成功'))    
        

#主程式
import os
if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5000))
    #app.run(host='0.0.0.0', port=port)
    app.run(debug=True)

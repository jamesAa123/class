import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

# 讀取 Line Bot 設定檔
from line_bot_config import CHANNEL_ACCESS_TOKEN

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler('61f20b3b089ebbadfe68534f659693e2')  # 請替換為你的 Channel Secret

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if '課表' in event.message.text:
        generate_class_schedule_image()
        image_message = ImageSendMessage(
            original_content_url='https://img.onl/udYrTE',  # 請替換為你部署的圖片 URL
            preview_image_url='https://img.onl/udYrTE'  # 請替換為你部署的圖片 URL
        )
        line_bot_api.reply_message(event.reply_token, image_message)
    else:
        reply_message = '我不太了解你的訊息。'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

def generate_class_schedule_image():
    img = Image.new('RGB', (500, 300), color='white')
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    d.text((10, 10), "這是本週的課表：", fill=(0, 0, 0), font=font)
    img.save('images/class_schedule.png')

if __name__ == "__main__":
    app.run()

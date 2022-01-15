import os

from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import JoinEvent, MessageEvent, TextMessage, TextSendMessage

from leave_reporter.server import create_report


APP = Flask(__name__)
LINE_BOT_API = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
HANDLER = WebhookHandler(os.environ['CHANNEL_SECRET'])
GROUP_ID = os.environ.get('GROUP_ID', None)


@HANDLER.add(JoinEvent)
def handle_join(event):
    GROUP_ID = event.source.group_id
    print(f'Group ID obtained: {GROUP_ID=}')

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if msg == '開始回報':
        reply = 'https://forms.gle/foKhtWvw6SC7TFV69'
    elif msg == '彙整':
        reply = create_report()
    else:
        return
    LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(text=reply))


@APP.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    HANDLER.handle(body, signature)
    return 'OK'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    APP.run(host='0.0.0.0', port=port)

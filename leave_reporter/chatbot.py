import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import JoinEvent, MessageEvent, TextMessage, TextSendMessage


APP = Flask(__name__)
LINE_BOT_API = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
HANDLER = WebhookHandler(os.environ['CHANNEL_SECRET'])
GROUP_ID = None


@HANDLER.add(JoinEvent)
def handle_join(event):
    GROUP_ID = event.source.group_id
    print(f'Obtained Group ID: {GROUP_ID}')

@APP.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    HANDLER.handle(body, signature)
    return 'OK'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    APP.run(host='0.0.0.0', port=port)

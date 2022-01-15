import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import JoinEvent, MessageEvent, TextMessage, TextSendMessage


app = Flask(__name__)
LINE_BOT_API = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
HANDLER = WebhookHandler(os.environ['CHANNEL_SECRET'])


@HANDLER.add(JoinEvent)
def handle_join(event):
    group_id = event.source.group_id
    app.logger.info(f'Obtained Group ID: {group_id}')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info(f'Request body: {body}')
    HANDLER.handle(body, signature)


if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

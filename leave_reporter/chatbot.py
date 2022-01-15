import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import JoinEvent, MessageEvent, TextMessage, TextSendMessage


app = Flask(__name__)
LINE_BOT_API = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
HANDLER = WebhookHandler(os.environ['CHANNEL_SECRET'])


@HANDLER.add(JoinEvent)
def handle_join(event):
    group_id = event.source.group_id
    app.logger.info(f'Obtained Group ID: {group_id}')

@HANDLER.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply = event.message.text
    LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(text=reply))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info(f'Request body: {body}')

    try:
        HANDLER.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

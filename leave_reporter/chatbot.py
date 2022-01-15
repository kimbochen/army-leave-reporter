import os
import time
from multiprocessing import Process, Array

from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import JoinEvent, TextSendMessage


APP = Flask(__name__)
LINE_BOT_API = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
HANDLER = WebhookHandler(os.environ['CHANNEL_SECRET'])

INIT_ID = 'z' * 33
GROUP_ID = Array('c', INIT_ID.encode('utf-8'))


@HANDLER.add(JoinEvent)
def handle_join(event):
    GROUP_ID = event.source.group_id
    print(f'Obtained Group ID: {GROUP_ID}')

@APP.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    HANDLER.handle(body, signature)
    return 'OK'


def reminder():
    print('Started reminder.')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    flask_p = Process(target=APP.run, args=('0.0.0.0', port))
    flask_p.start()

    while GROUP_ID == INIT_ID:
        time.sleep(1)
    else:
        flask_p.terminate()
        flask_p.join()
        reminder()

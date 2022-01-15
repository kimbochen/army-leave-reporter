import os
import time
from multiprocessing import Process, Array

import schedule
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import JoinEvent, TextSendMessage

from leave_reporter.server import create_report


APP = Flask(__name__)
LINE_BOT_API = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
HANDLER = WebhookHandler(os.environ['CHANNEL_SECRET'])

INIT_ID = b'z' * 33
GROUP_ID = Array('c', INIT_ID)


@HANDLER.add(JoinEvent)
def handle_join(event):
    GROUP_ID.value = event.source.group_id.encode()
    print(f'Obtained Group ID')

@APP.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    HANDLER.handle(body, signature)
    return 'OK'


def send_form(group_id):
    LINE_BOT_API.push_message(group_id, TextSendMessage(text='https://forms.gle/foKhtWvw6SC7TFV69'))

def send_report(group_id):
    report = create_report()
    LINE_BOT_API.push_message(group_id, TextSendMessage(text=report))

def reminder():
    print(f'Started reminder.')
    group_id = GROUP_ID.value.decode()

    schedule.every().day.at('18:40').do(send_form, group_id=group_id)  # Taipei Timezone!
    schedule.every().day.at('19:40').do(send_report, group_id=group_id)  # Taipei Timezone!

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    flask_p = Process(target=APP.run, args=('0.0.0.0', port))
    flask_p.start()

    while GROUP_ID.value == INIT_ID:
        time.sleep(1)
    else:
        flask_p.terminate()
        flask_p.join()
        reminder()

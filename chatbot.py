# -*- coding: UTF-8 -*-

import os

from flask import Flask, request
from googleapiclient.discovery import build
from linebot import LineBotApi, WebhookHandler
from linebot.models import JoinEvent, MessageEvent, TextMessage, TextSendMessage


def create_report():
    spreadsheet_id = os.environ['SPREADSHEET_ID']
    api_key = os.environ['API_KEY']
    data_range = f"\'{os.environ['SHEET_NAME']}\'!B2:C"

    service = build('sheets', 'v4', developerKey=api_key)
    sheet = service.spreadsheets()
    results = sheet.values().get(spreadsheetId=spreadsheet_id, range=data_range).execute()
    records = sorted(results['values'], key=lambda r: r[0])  # [Name, Content]

    content = [f'{name}\n{response}' for name, response in records]
    header = f'''收假回報
兵器連 第四班
應到 13 員 實到 {len(content)} 員
看診人數：0
發燒人數：0
事故人數：0
———————————————\n'''
    report = header + '\n\n'.join(content)

    return report


APP = Flask(__name__)
LINE_BOT_API = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
HANDLER = WebhookHandler(os.environ['CHANNEL_SECRET'])
GROUP_ID = os.environ.get('GROUP_ID', None)

@HANDLER.add(JoinEvent)
def handle_join(event):
    GROUP_ID = event.source.group_id
    print(f'Group ID obtained: {GROUP_ID=}')

@HANDLER.add(MessageEvent, message=TextMessage)
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

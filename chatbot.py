# -*- coding: UTF-8 -*-

import os
from datetime import datetime

from flask import Flask, request
from googleapiclient.discovery import build
from linebot import LineBotApi, WebhookHandler
from linebot.models import JoinEvent, MessageEvent, TextMessage, TextSendMessage


REPORT_MSG = f'''回報連結：
{os.environ['FORM_LINK']}
確認回報情形：
https://docs.google.com/spreadsheets/d/{os.environ["SPREADSHEET_ID"]}
這是我的最後一次了各位'''

CADENCE_CALLS = [
    '威武', '嚴肅', '剛直', '安靜', '堅強',
    '確實', '速決', '沈著', '忍耐', '機警'
]


def create_report():
    spreadsheet_id = os.environ['SPREADSHEET_ID']
    api_key = os.environ['API_KEY']
    data_range = f"\'{os.environ['SHEET_NAME']}\'!B2:C"

    service = build('sheets', 'v4', developerKey=api_key)
    sheet = service.spreadsheets()
    results = sheet.values().get(spreadsheetId=spreadsheet_id, range=data_range).execute()

    if 'values' in results.keys():
        records = sorted(results['values'], key=lambda r: r[0])  # [Name, Content]
        content = [f'{name}\n{response}' for name, response in records]
    else:
        content = []

    now = datetime.now()
    header = f'''{now:%m/%d} {now:%H%M} 收假回報
兵器連 第四班
應到 13 員 實到 {len(content)} 員
看診人數：0
發燒人數：0
事故人數：0
———————————————
'''
    report = header + '\n\n'.join(content)

    return report


APP = Flask(__name__)
LINE_BOT_API = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
HANDLER = WebhookHandler(os.environ['CHANNEL_SECRET'])

@HANDLER.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    if msg == '開始回報':
        reply_msg = REPORT_MSG
    elif msg == '彙整':
        reply_msg = create_report()
    elif msg == '精神答數':
        reply_msg = '雄壯'
    elif msg in CADENCE_CALLS:
        idx = CADENCE_CALLS.index(msg)
        reply_msg = CADENCE_CALLS[idx + 1]
    elif '以為' in msg:
        reply_msg = '你以為，又你以為'
    else:
        return

    LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(reply_msg))


@APP.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    HANDLER.handle(body, signature)
    return 'OK'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    APP.run(host='0.0.0.0', port=port)

# -*- coding: UTF-8 -*-

import os
from googleapiclient.discovery import build


def create_report():
    spreadsheet_id = os.environ['SPREADSHEET_ID']
    api_key = os.environ['API_KEY']

    service = build('sheets', 'v4', developerKey=api_key)
    sheet = service.spreadsheets()
    results = sheet.values().get(spreadsheetId=spreadsheet_id, range='A2:C').execute()
    records = sorted(results['values'], key=lambda r: r[1])  # [Timestamp, Name, Content]

    content = [f'{name}\n{response}' for _, name, response in records]
    header = f'''放假回報
兵器連 第四班
應到 13 員 實到 {len(content)} 員
看診人數：0
發燒人數：0
事故人數：0
———————————————\n'''
    report = header + '\n\n'.join(content)

    return report


if __name__ == '__main__':
    print(create_report())

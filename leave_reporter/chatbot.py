import os
import logging

from linebot import LineBotApi, WebhookHandler


LINE_BOT_API = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
HANDLER = WebhookHandler(os.environ['CHANNEL_SECRET'])

@HANDLER.add(JoinEvent, message=TextMessage)
def handle_join(event):
    group_id = event.source.group_id
    loggin.info(f'Obtained Group ID: {group_id}')

def main():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    logging.info(f'Request body: {body}')
    HANDLER.handle(body, signature)


if __name__ == '__main__':
    main()

# -*- coding: UTF-8 -*-

from datetime import datetime
from os import environ

import pytz
import schedule

from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from constants import WEEKDAY_CN, USERS


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    uid = db.Column(db.String(80), primary_key=True, nullable=False)
    army_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'{self.army_id} {self.username}'

class Post(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.army_id'), nullable=False)

    def __repr__(self):
        return f'{self.body}'


CHANNEL_ACCESS_TOKEN = environ.get('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = environ.get('CHANNEL_SECRET')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    if msg.startswith('回報'):
        user = User.query.filter_by(uid=event.source.user_id).first()
        post = Post(body=msg[3:], author_id=user.army_id)
        db.session.add(post)
        db.session.commit()
        reply = f'收到回報：\n{post}'
    elif msg == '我是誰':
        reply = (
            f'user_id: {event.source.user_id}\n請將資料填寫至這個試算表：\n'
            'https://docs.google.com/spreadsheets/d/13uDJ15ZPIVNsbYC2w2ri6N5jFjsm5L42V-st0rUE_lc'
        )
    elif msg == '彙整':
        reply = create_report()
    else:
        reply = 'Excellent, 秉義'

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))


def create_report():
    posts = Post.query.order_by(Post.author_id).all()
    users = User.query.order_by(User.army_id).all()
    reports = [ f'{user}\n{post}' for user, post in zip(users, posts)]
    reply = '\n'.join(reports)

    now = datetime.now(tz=pytz.timezone('Asia/Taipei'))
    day = WEEKDAY_CN[f'{now:%a}']
    header = f'''兵器連第四班 {now:%m/%d} ({day}) {now:%H%M} 回報
應報告 13 員，實報 {len(reports)} 員
看診人數：0 
發燒人數：0
事故人數：0
———————————————'''

    return f'{header}\n{reply}'


def init_db():
    db.create_all()
    for user_kwargs in USERS:
        db.session.add(User(**user_kwargs))
    db.session.commit()


if __name__ == "__main__":
    init_db()
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    # notify_time = [
    #     '184000', '170000', '171000', '172900'
    # ]
    # now = datetime.now(tz=pytz.timezone('Asia/Taipei')).time()
    # if f'{now:%H%M%S}' in notify_time:
    try:
        line_bot_api.push_message('Uc2f286d0a61d78ba9059875cc88e5953', TextSendMessage(text='開始回報'))
    except LineBotApiError as e:
        print(e)
        abort(500)

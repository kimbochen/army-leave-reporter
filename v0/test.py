# -*- coding: UTF-8 -*-

from app import User, Post, db

db.create_all()


db.session.add(User(army_id=44051, username='陳騰鴻'))
db.session.add(Post(body='你好我好大家好', author_id=44051))
db.session.commit()

db.session.add(User(army_id=44050, username='劉哲維'))
db.session.add(Post(body='舒芙雷了啦', author_id=44050))
db.session.commit()

db.session.add(User(army_id=44045, username='張元'))
db.session.add(Post(body='操', author_id=44049))
db.session.commit()


posts = Post.query.order_by(Post.author_id).all()
users = User.query.order_by(User.army_id).all()
for user, post in zip(users, posts):
    print(f'{user}\n{post}\n')

db.drop_all()

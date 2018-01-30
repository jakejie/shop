# coding:utf-8
from app import db, login_manager
import hashlib
import time
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# 用户表
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 序号
    email = db.Column(db.String(64), unique=True, index=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号码
    username = db.Column(db.String(64), unique=True, index=True)  # 用户名
    password = db.Column(db.String(256))  # 密码
    password_hash = db.Column(db.String(128), unique=True)  # 密码 哈希
    avatar_hash = db.Column(db.String(32))
    image = db.Column(db.TEXT)  # 图像
    account_atatus = db.Column(db.String(4))  # 账号状态
    activate = db.Column(db.String(4), default="1")  # 1表示未激活 2表示已经激活
    ac_type = db.Column(db.String(4), default="1")  # 1表示普通用户 2表示管理员后台账号
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 注册时间
    info = db.Column(db.Text)  # 个性简介
    member_grade = db.Column(db.String(4), default="0")  # 会员等级
    account_point = db.Column(db.Integer, default=0)  # 会员积分
    # banas = db.
    # （设置外键的第二步）
    # userlogs = db.relationship('userlog', backref='user')  # 会员日志外键关系关联
    # comments = db.relationship('Comment', backref='user')  # 评论外键关系关联
    # moviecols = db.relationship('Moviecol', backref='user')  # 收藏外键关系关联
    db.relationship()

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def insert_admin(email, phone, username, password, ac_type="2", activate="2"):
        user = User(email=email, phone=phone, username=username,
                    password=password, ac_type=ac_type, activate=activate)
        db.session.add(user)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    def gravatar(self, size=40, default='identicon', rating='g'):
        # if request.is_secure:
        #     url = 'https://secure.gravatar.com/avatar'
        # else:
        #     url = 'http://www.gravatar.com/avatar'
        url = 'http://gravatar.duoshuo.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)


# 登陆的钩子
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 订单列表
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 序号
    add_time = db.Column(db.DATETIME)

# 商品列表
class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 序号

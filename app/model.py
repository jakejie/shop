# coding:utf-8
from app import db, login_manager
import hashlib
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# 用户表
class User(UserMixin, db.Model):
    __tablename__ = 'user'
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
    # （设置外键的第二步）
    address = db.relationship('Address', backref='users')  # 会员收货地址外键关系关联

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
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)  # 序号
    add_time = db.Column(db.DATETIME, default=datetime.now())
    address = db.Column(db.Integer, db.ForeignKey('address.id'))  # 绑定外键 对应哪个地址的订单
    good = db.Column(db.Integer, db.ForeignKey('goods.id'))  # 绑定外键 对应哪个商品的订单
    user = db.Column(db.Integer, db.ForeignKey('user.id'))  # 绑定外键 对应哪个用户的订单


# 商品列表
class Goods(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer, primary_key=True)  # 序号
    name = db.Column(db.String(512), unique=True)  # 商品名称
    view_num = db.Column(db.Integer, unique=True, default=1)  # 浏览次数


# 收货地址列表
class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(512), unique=True)  # 省份
    city = db.Column(db.String(512), unique=True)
    area = db.Column(db.String(512), unique=True)
    address = db.Column(db.String(512), unique=True)
    phone = db.Column(db.String(20), unique=True)
    remarks = db.Column(db.String(512))
    # 外键第二步
    users = db.Column(db.String(128), db.ForeignKey('user.username'))


# 大分类列表
class TagList(db.Model):
    __tablename__ = 'tag_list'
    id = db.Column(db.Integer, primary_key=True)  # 序号
    name = db.Column(db.String(128), unique=True)
    # 外键第二步
    tag_id = db.relationship('Tag', backref='tag_list')  # 底下分类所属分类外键关联关系


# 小分类
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)  # 序号
    name = db.Column(db.String(128), unique=True)
    # 外键第一步
    f_name = db.Column(db.String(128), db.ForeignKey('tag_list.name'))


# 页面统计数据
class Count(db.Model):
    __tablename__ = 'count'
    id = db.Column(db.Integer, primary_key=True)  # 序号
    days = db.Column(db.Integer, default=1)  # 运行天数
    view = db.Column(db.Integer)  # 浏览次数
    goods_num = db.Column(db.Integer)  # 商品总数
    user_num = db.Column(db.Integer)  # 当前会员总数
    today_goods = db.Column(db.Integer)  # 今日新上架商品
    today_views = db.Column(db.Integer)  # 今日浏览次数
    local_people = db.Column(db.Integer)  # 当前在线人数
    max_people = db.Column(db.Integer)  # 最大同时在线人数
    max_people_time = db.Column(db.DATETIME, default=datetime.now())  # 最大同时在线人数日期


if __name__ == "__main__":
    db.create_all()

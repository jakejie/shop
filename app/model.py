# coding:utf-8
from app import db, login_manager
import hashlib
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import time


# 大分类列表==一级
class TagList(db.Model):
    __tablename__ = 'tag_list'
    id = db.Column(db.Integer, primary_key=True)  # 序号
    name = db.Column(db.String(128), unique=True)
    # 外键第二步
    f_name = db.relationship("Tags", backref='tag_list')  # 底下分类所属分类外键关联关系


# 小分类==二级
class Tags(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)  # 序号
    name = db.Column(db.String(128), unique=True)
    # 外键第一步====绑定tag list
    f_name = db.Column(db.String(128), db.ForeignKey('tag_list.name'))  # 一级名称
    # 外键第二步
    t_name = db.relationship("Tag", backref='tags')  # 底下分类所属分类外键关联关系


# 再小分类==三级
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # 序号
    name = db.Column(db.String(128), unique=True)  # 三级分类
    # 外键第一步  绑定tag list
    t_name = db.Column(db.String(128), db.ForeignKey('tags.name'))  # 二级分类
    good_tag = db.relationship("Course", backref='tag')  # 底下分类所属分类外键关联关系


# 用户表
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 序号
    email = db.Column(db.String(64), unique=True, index=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号码
    username = db.Column(db.String(128), unique=True, index=True)  # 用户名
    birthday = db.Column(db.DATE)  # 出生日期
    sex = db.Column(db.String(32))  # 性别
    password = db.Column(db.String(256))  # 密码
    pwd = db.Column(db.String(256))
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
    uuid = db.Column(db.String(1024))
    # （设置外键的第二步）
    users_id = db.relationship('Address')  # 会员收货地址外键关系关联
    user_order = db.relationship('Orders')  # 订单信息外键关系关联
    comment_user = db.relationship('Comment', backref='user')  # 会员评论信息外键关系关联
    user_logs = db.relationship('UserLog', backref='user')  # 会员登陆日志信息外键关系关联
    user_message = db.relationship('Message', backref='user')  # 会员登陆日志信息外键关系关联
    user_car = db.relationship('BuyCar')  # 购物车外键关系关联
    detail_user = db.relationship('Detail')  # 订单商品购买人 外键关系关联
    col_user = db.relationship('Collect', backref='user')  # 收藏商品对应用户

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def insert_admin(email, phone, username, password, ac_type="2", activate="2"):
        user = User(email=email, phone=phone, username=username,
                    password=password, ac_type=ac_type, activate=activate)
        db.session.add(user)
        db.session.commit()

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')
    #
    # @password.setter
    # def password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def verify_password(self, password):
    #     return check_password_hash(self.password_hash, password)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    def gravatar(self, size=40, default='identicon', rating='g'):
        pass

    def check_pwd(self, password):  # 检验密码
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)

    def check_user(self, username):  # 检验用户名是否存在
        count = User.query.filter_by(username=username).count()
        if count == 1:
            return True
        else:
            return False


# 收货地址列表
class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(512))  # 省份
    city = db.Column(db.String(512))  # 城市
    area = db.Column(db.String(512))  # 地区
    address = db.Column(db.String(512))  # 街道等详细位置
    phone = db.Column(db.String(20))  # 收货电话
    name = db.Column(db.String(128))  # 收货人姓名
    remarks = db.Column(db.String(512))
    default_add = db.Column(db.Integer, default=1)  # 是否为默认地址 1表示默认地址 0表示非默认地址
    add_time = db.Column(db.DATETIME, default=datetime.now())  # 数据添加时间
    # 外键第二步
    users_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# 订单列表
class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)  # 序号
    add_time = db.Column(db.DATETIME)  # 提交订单时间
    order_id = db.Column(db.BIGINT, unique=True)  # 订单id 根据user id + 时间戳生成
    address = db.Column(db.String(512))  # 使用注册的用户的邮箱//收件人姓名就行 绑定外键 对应哪个地址的订单
    remark = db.Column(db.String(512))  # 添加订单备注
    user = db.Column(db.Integer, db.ForeignKey('user.id'))  # 绑定外键 对应哪个用户的订单
    user_detail = db.relationship("Detail", backref='orders')  # 该订单对应的商品 外键关联
    times = db.Column(db.BIGINT)
    pay = db.Column(db.Integer, default=0)  # 是否支付成功 0=待支付 1=支付成功
    cancel = db.Column(db.Integer, default=0)  # 订单是否取消 0=未取消 1=已经取消的订单
    alipay = db.Column(db.String(256))  # 支付宝支付后的订单号 用来验证是否收款
    pay_remark = db.Column(db.String(1024))  # 用户提交支付状态的时候的备注信息


# 订单里面的商品列表 一个订单有多个商品
class Detail(db.Model):
    __tablename__ = 'detail'
    id = db.Column(db.Integer, primary_key=True)
    add_time = db.Column(db.DATETIME)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))  # 该订单对应的商品id
    num = db.Column(db.Integer)  # 购买该商品的数量
    orderId = db.Column(db.Integer, db.ForeignKey('orders.order_id'))  # 该订单的id
    user = db.Column(db.Integer, db.ForeignKey('user.id'))  # 哪个用户购买了该商品
    price = db.Column(db.String(32))  # 该订单对应金额


# 学校/机构--》老师--》课程


# 课程所属学校/机构
class School(db.Model):
    __tablename__ = 'school'
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(512), unique=True)  # 学校名字
    school_image = db.Column(db.String(256))  # 学校图片
    school_info = db.Column(db.String(512))  # 一句话简介
    school_address = db.Column(db.String(512))  # 学校地址
    course_num = db.Column(db.Integer)  # 课程数量
    teacher_num = db.Column(db.Integer, default=1)  # 讲师数量
    student_num = db.Column(db.Integer)  # 学生数量
    start = db.Column(db.FLOAT)  # 推荐指数 几星级

    school_id = db.relationship('SchoolCourse')
    teacher = db.relationship('Teacher')
    course_sch = db.relationship('Course')


# 老师所属学校/机构
class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(512), unique=True)  # 讲师名字
    teacher_job = db.Column(db.String(512))  # 讲师工作职位
    teacher_company = db.Column(db.String(512), db.ForeignKey('school.school_name'))  # 讲师所在学校
    teacher_type = db.Column(db.String(512))  # 讲师类型/是否金牌讲师/讲师等级
    teacher_year = db.Column(db.Integer)  # 工作年限
    teacher_age = db.Column(db.Integer)  # 年龄
    tech_point = db.Column(db.String(512))  # 讲学特点
    teacher_image = db.Column(db.String(512))  # 讲师主页图片
    teacher_course = db.relationship('Course')
    add_time = db.Column(db.DATETIME, default=datetime.now())


# 机构/学校对应经典课程
class SchoolCourse(db.Model):
    __tablename__ = 'school_course'
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    good_course = db.Column(db.String(512), db.ForeignKey('course.course_name'))  # 经典课程


# 商品列表/课程列表
class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)  # 序号
    course_id = db.Column(db.Integer, unique=True)  # 商品id
    course_name = db.Column(db.String(512), unique=True)  # 商品名称
    introduce = db.Column(db.String(512))  # 课程简介
    image = db.Column(db.String(256), unique=True)  # 商品图片 文件名唯一
    good_tag = db.Column(db.String(128), db.ForeignKey('tag.name'))  # 商品所属分类

    long_time = db.Column(db.String(128))  # 课程时长
    study_num = db.Column(db.Integer)  # 学习人数  购买人数
    teacher_name = db.Column(db.String(512), db.ForeignKey('teacher.teacher_name'))  # 该课程对应讲师
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))  # 该课程对应的机构/学校
    difficulty = db.Column(db.Integer)  # 难度
    # 1 入门 2 初级 3 中级 4 高级
    chap_num = db.Column(db.Integer)  # 该课程章节数
    price = db.Column(db.FLOAT(16))  # 现价
    old_price = db.Column(db.FLOAT(16))  # 原价
    start = db.Column(db.Integer)  # 星级>>>1-5星
    discount = db.Column(db.FLOAT(32))  # 折扣
    add_time = db.Column(db.DATETIME, default=datetime.now())  # 上架时间
    skull_num = db.Column(db.Integer, default=0)  # 库存
    sales = db.Column(db.Integer, default=0)  # 销量
    view_num = db.Column(db.Integer, default=1)  # 浏览次数
    comment_num = db.Column(db.Integer, default=0)  # 评论数量
    course_info = db.Column(db.Text)  # 商品介绍
    share_link = db.Column(db.String(256))  # 分享链接
    get_secure = db.Column(db.String(256))  # 提取密码
    target = db.Column(db.Integer, default=1)  # 商品是否上架 0表示未上架 1表示已经上架 默认直接上架商品
    detail = db.Column(db.Text)  # 课程详情介绍
    # 外键关联第二步
    comment_good = db.relationship('Comment', backref='course')
    course_ids = db.relationship('Detail', backref='course')
    # course_orders = db.relationship('Orders', backref='course')
    car_id = db.relationship('BuyCar', backref='course')
    good_course = db.relationship('SchoolCourse', backref='course')
    course_chapter = db.relationship('CourseChapters')


# 课程章节数 章节列表
class CourseChapters(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)  # 序号
    course = db.Column(db.Integer, db.ForeignKey('course.course_id'))
    chapter_id = db.Column(db.Integer)  # 章节序号
    chapter_name = db.Column(db.String(512))  # 章节名称
    long_time = db.Column(db.Integer)  # 该章节时长


# 购物车
class BuyCar(db.Model):
    __tablename__ = 'buycar'
    id = db.Column(db.Integer, primary_key=True)
    add_time = db.Column(db.DATETIME, default=datetime.now())  # 加入购物车时间
    num = db.Column(db.Integer, default=1)  # 商品数量 默认只购买一件 应该禁止修改
    price = db.Column(db.FLOAT(16))
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))  # 购物车商品名称
    user_car = db.Column(db.Integer, db.ForeignKey('user.id'))  # 哪个用户购物车里的商品


# 用户收藏商品/课程列表
class Collect(db.Model):
    __tablename__ = 'collect'
    id = db.Column(db.Integer, primary_key=True)
    col_type = db.Column(db.Integer)  # 收藏的是课程还是机构 1=课程 2=机构 3=老师
    add_time = db.Column(db.DATETIME, default=datetime.now())  # 收藏时间
    course_id = db.Column(db.Integer)  # 收藏商品ID/机构id/老师id
    users = db.Column(db.Integer, db.ForeignKey('user.id'))  # 哪个用户收藏的商品


# 评论列表
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)  # 序号
    content = db.Column(db.Text)  # 评论内容
    add_time = db.Column(db.DATETIME, default=datetime.now())  # 评论时间
    fab = db.Column(db.Integer, default=0)  # 点赞数
    replay = db.Column(db.Text)  # 回复
    comment_course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))  # 所评论的商品的id
    users = db.Column(db.Integer, db.ForeignKey('user.id'))  # 评论用户


# 页面统计数据
class Count(db.Model):
    __tablename__ = 'count'
    id = db.Column(db.Integer, primary_key=True)  # 序号
    days = db.Column(db.Integer, default=1)  # 运行天数
    view = db.Column(db.Integer)  # 浏览次数

    today_order = db.Column(db.Integer)  # 今日订单数
    today_course = db.Column(db.Integer)  # 今日新上架商品
    today_views = db.Column(db.Integer)  # 今日浏览次数 今日访客
    today_vip = db.Column(db.Integer)  # 今日新增注册会员

    order_num = db.Column(db.Integer)  # 订单总数
    course_num = db.Column(db.Integer)  # 商品总数
    view_num = db.Column(db.Integer)  # 历时浏览次数
    user_num = db.Column(db.Integer)  # 当前会员总数

    local_people = db.Column(db.Integer)  # 当前在线人数
    max_people = db.Column(db.Integer)  # 最大同时在线人数
    max_people_time = db.Column(db.DATETIME, default=datetime.now())  # 最大同时在线人数日期


# 登陆日志
class UserLog(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    ip_add = db.Column(db.String(32))  # 登陆IP地址
    add_time = db.Column(db.DATETIME, default=datetime.now())  # 记录时间
    user_logs = db.Column(db.Integer, db.ForeignKey('user.id'))  # 登陆用户
    remark = db.Column(db.String(512))  # 操作内容 标记备注


# 通知类消息
class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    add_time = db.Column(db.DATETIME, default=datetime.now())
    mark = db.Column(db.Text)  # 消息通知内容
    user_mess = db.Column(db.Integer, db.ForeignKey('user.id'))  # 对应用户


# 登陆的钩子  用户认证的回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 登陆用户需要进行邮箱验证方可正常进行登陆
def generate_confirmation_token(self, expiration=3600):
    # 这个函数需要两个参数，一个密匙，从配置文件获取，一个时间，这里1小时
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    # 为ID生成一个加密签名，然后再对数据和签名进行序列化，生成令牌版字符串（就是一长串乱七八糟的东西）,然后返回
    return s.dumps({'confirm': self.id})


def confirm(self, token):
    # 激活
    s = Serializer(current_app.config['SECRET_KEY'])
    # 传入和刚才一样的密匙，解码要用
    try:
        data = s.loads(token)  # 解码
    except:
        return False
    if data.get('confirm') != self.id:
        return False
    self.confirmed = True  # 解的码和已经登录的账号ID相等时操作数据库改变User.confirmed的值为True
    db.session.add(self)
    return True  # 激活成功返回True


# if __name__ == "__main__":
#     db.create_all()
#     db.upgrade()
# python manage.py db migrate
# python manage.py db upgrade
# python manage.py deploy
#

# pass
"""
{"tag": 'IT/互联网/计算机', "name": '编程语言', "detail": 'C/C++'}
{"tag": 'IT/互联网/计算机', "name": '编程语言', "detail": 'VC/MFC'}
{"tag": 'IT/互联网/计算机', "name": '编程语言', "detail": 'JAVA'}
{"tag": 'IT/互联网/计算机', "name": '编程语言', "detail": 'Python'}
{"tag": 'IT/互联网/计算机', "name": '编程语言', "detail": 'PHP'}
{"tag": 'IT/互联网/计算机', "name": '编程语言', "detail": '脚本语言'}
{"tag": 'IT/互联网/计算机', "name": '编程语言', "detail": 'Objective-C'}
{"tag": 'IT/互联网/计算机', "name": '常用软件', "detail": 'Photoshop'}
{"tag": 'IT/互联网/计算机', "name": '常用软件', "detail": '3Dmax'}
{"tag": 'IT/互联网/计算机', "name": '常用软件', "detail": 'Illustrator'}
{"tag": 'IT/互联网/计算机', "name": '常用软件', "detail": 'Flash'}
{"tag": 'IT/互联网/计算机', "name": '常用软件', "detail": 'Dreamweaver'}
{"tag": 'IT/互联网/计算机', "name": '常用软件', "detail": 'Maya'}
{"tag": 'IT/互联网/计算机', "name": '常用软件', "detail": 'Axure'}
{"tag": 'IT/互联网/计算机', "name": '设计制作', "detail": '平面设计'}
{"tag": 'IT/互联网/计算机', "name": '设计制作', "detail": '网站制作'}
{"tag": 'IT/互联网/计算机', "name": '设计制作', "detail": '页面设计'}
{"tag": 'IT/互联网/计算机', "name": '设计制作', "detail": '游戏设计'}
{"tag": 'IT/互联网/计算机', "name": '设计制作', "detail": '三维设计'}
{"tag": 'IT/互联网/计算机', "name": '设计制作', "detail": 'CG动画'}
{"tag": 'IT/互联网/计算机', "name": '数 据 库', "detail": 'Oracle'}
{"tag": 'IT/互联网/计算机', "name": '数 据 库', "detail": 'SQL Server'}
{"tag": 'IT/互联网/计算机', "name": '数 据 库', "detail": 'MySQL'}
{"tag": 'IT/互联网/计算机', "name": '系统运维', "detail": 'Linux'}
{"tag": 'IT/互联网/计算机', "name": '系统运维', "detail": 'Vmware'}
{"tag": 'IT/互联网/计算机', "name": '系统运维', "detail": 'Windows'}
{"tag": 'IT/互联网/计算机', "name": '系统运维', "detail": '网络管理'}
{"tag": 'IT/互联网/计算机', "name": '系统运维', "detail": 'Exchange'}
{"tag": 'IT/互联网/计算机', "name": '移动互联网', "detail": 'Android'}
{"tag": 'IT/互联网/计算机', "name": '移动互联网', "detail": 'IOS'}
{"tag": 'IT/互联网/计算机', "name": '移动互联网', "detail": 'Webapp'}
{"tag": 'IT/互联网/计算机', "name": '产品运营', "detail": '产品设计'}
{"tag": 'IT/互联网/计算机', "name": '产品运营', "detail": '  网站编辑'}
{"tag": 'IT/互联网/计算机', "name": '产品运营', "detail": '数据分析'}
{"tag": 'IT/互联网/计算机', "name": '产品运营', "detail": '策划'}
{"tag": 'IT/互联网/计算机', "name": '其他', "detail": '网络安全'}
{"tag": 'IT/互联网/计算机', "name": '其他', "detail": '嵌入式培训'}
{"tag": 'IT/互联网/计算机', "name": '其他', "detail": '移动通信'}
{"tag": 'IT/互联网/计算机', "name": '其他', "detail": '云计算'}
{"tag": 'IT/互联网/计算机', "name": '其他', "detail": '系统架构'}
{"tag": '求职/职场办公技能', "name": '求职', "detail": '职业规划'}
{"tag": '求职/职场办公技能', "name": '求职', "detail": '求职简历'}
{"tag": '求职/职场办公技能', "name": '求职', "detail": '面试技巧'}
{"tag": '求职/职场办公技能', "name": '求职', "detail": '跳槽'}
{"tag": '求职/职场办公技能', "name": '求职', "detail": '就业指导'}
{"tag": '求职/职场办公技能', "name": '职场技能', "detail": '演讲与口才'}
{"tag": '求职/职场办公技能', "name": '职场技能', "detail": '自我表现'}
{"tag": '求职/职场办公技能', "name": '职场技能', "detail": '情绪管理'}
{"tag": '求职/职场办公技能', "name": '职场技能', "detail": '总结汇报'}
{"tag": '求职/职场办公技能', "name": '职场技能', "detail": '团队技能'}
{"tag": '求职/职场办公技能', "name": '职场技能', "detail": '管理技能'}
{"tag": '求职/职场办公技能', "name": '企业管理', "detail": '企业培训'}
{"tag": '求职/职场办公技能', "name": '企业管理', "detail": '财务/会计'}
{"tag": '求职/职场办公技能', "name": '企业管理', "detail": '人力资源管理'}
{"tag": '求职/职场办公技能', "name": '其他技能', "detail": '创业'}
{"tag": '求职/职场办公技能', "name": '其他技能', "detail": '职场礼仪'}
{"tag": '求职/职场办公技能', "name": '其他技能', "detail": '领导力培训'}
{"tag": '求职/职场办公技能', "name": '办公软件', "detail": 'word'}
{"tag": '求职/职场办公技能', "name": '办公软件', "detail": 'excel'}
{"tag": '求职/职场办公技能', "name": '办公软件', "detail": 'PPT'}
{"tag": '求职/职场办公技能', "name": '办公软件', "detail": 'Visio'}
{"tag": '求职/职场办公技能', "name": '办公软件', "detail": 'access'}
{"tag": '求职/职场办公技能', "name": '办公软件', "detail": 'WPS'}
{"tag": '求职/职场办公技能', "name": '电脑基础', "detail": '基础操作'}
{"tag": '求职/职场办公技能', "name": '电脑基础', "detail": '电脑培训'}
{"tag": '求职/职场办公技能', "name": '电脑基础', "detail": '电脑选购'}
{"tag": '求职/职场办公技能', "name": '电脑基础', "detail": '软件技术'}
{"tag": '求职/职场办公技能', "name": '电脑基础', "detail": '装机技巧'}
{"tag": '语言学习', "name": '英语', "detail": '英语口语'}
{"tag": '语言学习', "name": '英语', "detail": '英语词汇'}
{"tag": '语言学习', "name": '英语', "detail": '英语入门'}
{"tag": '语言学习', "name": '英语', "detail": '职场英语'}
{"tag": '语言学习', "name": '英语', "detail": '行业英语'}
{"tag": '语言学习', "name": '英语', "detail": '职称英语'}
{"tag": '语言学习', "name": '日语', "detail": '日语入门'}
{"tag": '语言学习', "name": '日语', "detail": '日语口语'}
{"tag": '语言学习', "name": '日语', "detail": '日语考试'}
{"tag": '语言学习', "name": '日语', "detail": '日语语法'}
{"tag": '语言学习', "name": '日语', "detail": '日语词汇'}
{"tag": '语言学习', "name": '日语', "detail": '新标日'}
{"tag": '语言学习', "name": '日语', "detail": '大家的日语'}
{"tag": '语言学习', "name": '韩语', "detail": '韩语入门'}
{"tag": '语言学习', "name": '韩语', "detail": '韩语口语'}
{"tag": '语言学习', "name": '韩语', "detail": '韩语语法'}
{"tag": '语言学习', "name": '韩语', "detail": '韩语词汇'}
{"tag": '语言学习', "name": '韩语', "detail": '韩语考试'}
{"tag": '语言学习', "name": '法语', "detail": '法语入门'}
{"tag": '语言学习', "name": '法语', "detail": '法语口语'}
{"tag": '语言学习', "name": '法语', "detail": '法语词汇'}
{"tag": '语言学习', "name": '法语', "detail": '法语考试'}
{"tag": '语言学习', "name": '小语种', "detail": '粤语'}
{"tag": '语言学习', "name": '小语种', "detail": '德语'}
{"tag": '语言学习', "name": '小语种', "detail": '西班牙语'}
{"tag": '语言学习', "name": '小语种', "detail": '汉语'}
{"tag": '语言学习', "name": '小语种', "detail": '其他'}
{"tag": '金融管理类市场/营销更多技能', "name": '金融投资', "detail": '理财'}
{"tag": '金融管理类市场/营销更多技能', "name": '金融投资', "detail": '基金'}
{"tag": '金融管理类市场/营销更多技能', "name": '金融投资', "detail": '黄金'}
{"tag": '金融管理类市场/营销更多技能', "name": '金融投资', "detail": '股票'}
{"tag": '金融管理类市场/营销更多技能', "name": '金融投资', "detail": '期货'}
{"tag": '金融管理类市场/营销更多技能', "name": '金融投资', "detail": '保险'}
{"tag": '金融管理类市场/营销更多技能', "name": '管 理 类', "detail": '工商管理'}
{"tag": '金融管理类市场/营销更多技能', "name": '管 理 类', "detail": '旅游管理'}
{"tag": '金融管理类市场/营销更多技能', "name": '管 理 类', "detail": '公共管理'}
{"tag": '金融管理类市场/营销更多技能', "name": '管 理 类', "detail": '其他'}
{"tag": '金融管理类市场/营销更多技能', "name": '网络营销', "detail": 'SEO'}
{"tag": '金融管理类市场/营销更多技能', "name": '网络营销', "detail": 'SEM'}
{"tag": '金融管理类市场/营销更多技能', "name": '网络营销', "detail": 'EDM'}
{"tag": '金融管理类市场/营销更多技能', "name": '网络营销', "detail": 'SNS'}
{"tag": '金融管理类市场/营销更多技能', "name": '网络营销', "detail": '淘宝营销'}
{"tag": '金融管理类市场/营销更多技能', "name": '网络营销', "detail": '微信营销'}
{"tag": '金融管理类市场/营销更多技能', "name": '网络营销', "detail": '数据库营销'}
{"tag": '金融管理类市场/营销更多技能', "name": '市场销售', "detail": '电子商务'}
{"tag": '金融管理类市场/营销更多技能', "name": '市场销售', "detail": '对外贸易'}
{"tag": '金融管理类市场/营销更多技能', "name": '市场销售', "detail": '市场营销'}
{"tag": '金融管理类市场/营销更多技能', "name": '市场销售', "detail": '推销/促销'}
{"tag": '金融管理类市场/营销更多技能', "name": '市场销售', "detail": '销售'}
{"tag": '金融管理类市场/营销更多技能', "name": '医疗保健', "detail": '中医'}
{"tag": '金融管理类市场/营销更多技能', "name": '医疗保健', "detail": '西医'}
{"tag": '金融管理类市场/营销更多技能', "name": '医疗保健', "detail": '临床医学'}
{"tag": '金融管理类市场/营销更多技能', "name": '医疗保健', "detail": '医药'}
{"tag": '金融管理类市场/营销更多技能', "name": '医疗保健', "detail": '保健/养生'}
{"tag": '金融管理类市场/营销更多技能', "name": '其他', "detail": '师资培训'}
{"tag": '金融管理类市场/营销更多技能', "name": '其他', "detail": '自动化'}
{"tag": '金融管理类市场/营销更多技能', "name": '其他', "detail": '电子'}
{"tag": '金融管理类市场/营销更多技能', "name": '其他', "detail": '文体教育'}
{"tag": '金融管理类市场/营销更多技能', "name": '其他', "detail": '驾驶技术'}
{"tag": '资格考试', "name": '财会考试', "detail": '会计证'}
{"tag": '资格考试', "name": '财会考试', "detail": '会计职称'}
{"tag": '资格考试', "name": '财会考试', "detail": '会计资格'}
{"tag": '资格考试', "name": '财会考试', "detail": '注册会计师'}
{"tag": '资格考试', "name": '财会考试', "detail": '美国会计考试'}
{"tag": '资格考试', "name": '财会考试', "detail": 'ACCA'}
{"tag": '资格考试', "name": '财会考试', "detail": '注册税务师'}
{"tag": '资格考试', "name": '财会考试', "detail": '审计师'}
{"tag": '资格考试', "name": '建造考试', "detail": '室内设计师'}
{"tag": '资格考试', "name": '建造考试', "detail": '注册建筑师'}
{"tag": '资格考试', "name": '建造考试', "detail": '一级建造师'}
{"tag": '资格考试', "name": '建造考试', "detail": '二级建造师'}
{"tag": '资格考试', "name": '建造考试', "detail": '监理工程师'}
{"tag": '资格考试', "name": '建造考试', "detail": '建筑师'}
{"tag": '资格考试', "name": '建造考试', "detail": '项目管理师'}
{"tag": '资格考试', "name": '建造考试', "detail": '咨询工程师'}
{"tag": '资格考试', "name": '建造考试', "detail": '造价师'}
{"tag": '资格考试', "name": '金融考试', "detail": '银行从业资格'}
{"tag": '资格考试', "name": '金融考试', "detail": '经济师'}
{"tag": '资格考试', "name": '金融考试', "detail": '金融分析师'}
{"tag": '资格考试', "name": '金融考试', "detail": '理财规划师'}
{"tag": '资格考试', "name": '金融考试', "detail": '精算师'}
{"tag": '资格考试', "name": '金融考试', "detail": '证券从业资格'}
{"tag": '资格考试', "name": '医药考试', "detail": '执业药师'}
{"tag": '资格考试', "name": '医药考试', "detail": '执业医师'}
{"tag": '资格考试', "name": '医药考试', "detail": '护士资格'}
{"tag": '资格考试', "name": '医药考试', "detail": '卫生资格'}
{"tag": '资格考试', "name": '企业管理类', "detail": '人力资源师'}
{"tag": '资格考试', "name": '企业管理类', "detail": '法律顾问'}
{"tag": '资格考试', "name": '企业管理类', "detail": '企业培训师'}
{"tag": '资格考试', "name": '职业资格类', "detail": '司法考试'}
{"tag": '资格考试', "name": '职业资格类', "detail": '教师资格证'}
{"tag": '资格考试', "name": '职业资格类', "detail": '其他'}
{"tag": '资格考试', "name": 'IT类考试', "detail": '资格认证'}
{"tag": '资格考试', "name": 'IT类考试', "detail": '软件水平考试'}
{"tag": '资格考试', "name": 'IT类考试', "detail": '职称考试'}
{"tag": '资格考试', "name": '其他', "detail": '营养师'}
{"tag": '资格考试', "name": '其他', "detail": '心理咨询师'}
{"tag": '资格考试', "name": '其他', "detail": '秘书资格证'}
{"tag": '资格考试', "name": '其他', "detail": '物流师'}
{"tag": '公务员更多考试', "name": '国考', "detail": '申论'}
{"tag": '公务员更多考试', "name": '国考', "detail": '行测'}
{"tag": '公务员更多考试', "name": '国考', "detail": '面试'}
{"tag": '公务员更多考试', "name": '省考', "detail": '申论'}
{"tag": '公务员更多考试', "name": '省考', "detail": '行测'}
{"tag": '公务员更多考试', "name": '省考', "detail": '面试'}
{"tag": '公务员更多考试', "name": '其他', "detail": '在职公务员'}
{"tag": '公务员更多考试', "name": '其他', "detail": '军转干'}
{"tag": '公务员更多考试', "name": '其他', "detail": '公选干'}
{"tag": '公务员更多考试', "name": '其他', "detail": '政法干警'}
{"tag": '公务员更多考试', "name": '学历教育', "detail": '自学考试'}
{"tag": '公务员更多考试', "name": '学历教育', "detail": '成人高考'}
{"tag": '公务员更多考试', "name": '学历教育', "detail": '在职研究生'}
{"tag": '公务员更多考试', "name": '学历教育', "detail": '其他'}
{"tag": '中小学家长专区', "name": '高中', "detail": '高一'}
{"tag": '中小学家长专区', "name": '高中', "detail": '高二'}
{"tag": '中小学家长专区', "name": '高中', "detail": '高三'}
{"tag": '中小学家长专区', "name": '高中', "detail": '高考'}
{"tag": '中小学家长专区', "name": '高中', "detail": '素质教育'}
{"tag": '中小学家长专区', "name": '初中', "detail": '初一'}
{"tag": '中小学家长专区', "name": '初中', "detail": '初二'}
{"tag": '中小学家长专区', "name": '初中', "detail": '初三'}
{"tag": '中小学家长专区', "name": '初中', "detail": '中考'}
{"tag": '中小学家长专区', "name": '初中', "detail": '素质教育'}
{"tag": '中小学家长专区', "name": '小学', "detail": '学前班'}
{"tag": '中小学家长专区', "name": '小学', "detail": '一年级'}
{"tag": '中小学家长专区', "name": '小学', "detail": '二年级'}
{"tag": '中小学家长专区', "name": '小学', "detail": '三年级'}
{"tag": '中小学家长专区', "name": '小学', "detail": '四年级'}
{"tag": '中小学家长专区', "name": '小学', "detail": '五年级'}
{"tag": '中小学家长专区', "name": '小学', "detail": '六年级'}
{"tag": '中小学家长专区', "name": '小学', "detail": '小升初'}
{"tag": '中小学家长专区', "name": '小学', "detail": '素质教育'}
{"tag": '中小学家长专区', "name": '品牌专区', "detail": '新概念'}
{"tag": '中小学家长专区', "name": '品牌专区', "detail": '三一口语'}
{"tag": '中小学家长专区', "name": '品牌专区', "detail": '剑桥英语'}
{"tag": '中小学家长专区', "name": '早期教育', "detail": '智慧父母'}
{"tag": '中小学家长专区', "name": '早期教育', "detail": '幼儿里程'}
{"tag": '中小学家长专区', "name": '早期教育', "detail": '亲子共读'}
{"tag": '中小学家长专区', "name": '早期教育', "detail": '能力开发'}
{"tag": '中小学家长专区', "name": '早期教育', "detail": '家庭医生'}
{"tag": '中小学家长专区', "name": '小学教育', "detail": '父母教育'}
{"tag": '中小学家长专区', "name": '小学教育', "detail": '家校结合'}
{"tag": '中小学家长专区', "name": '小学教育', "detail": '心理辅导'}
{"tag": '中小学家长专区', "name": '小学教育', "detail": '能力提升'}
{"tag": '中小学家长专区', "name": '小学教育', "detail": '亲子沟通'}
{"tag": '中小学家长专区', "name": '初中教育', "detail": '家教艺术'}
{"tag": '中小学家长专区', "name": '初中教育', "detail": '升学择校'}
{"tag": '中小学家长专区', "name": '初中教育', "detail": '成长交流'}
{"tag": '中小学家长专区', "name": '初中教育', "detail": '课业辅导'}
{"tag": '中小学家长专区', "name": '初中教育', "detail": '少男少女'}
{"tag": '中小学家长专区', "name": '高中教育', "detail": '高考专题'}
{"tag": '中小学家长专区', "name": '高中教育', "detail": '心理解密'}
{"tag": '中小学家长专区', "name": '高中教育', "detail": '沟通交流'}
{"tag": '中小学家长专区', "name": '高中教育', "detail": '花季雨季'}
{"tag": '中小学家长专区', "name": '高中教育', "detail": '招考指南'}
{"tag": '中小学家长专区', "name": '青 春 期', "detail": '沟通交流'}
{"tag": '中小学家长专区', "name": '青 春 期', "detail": '心理解密'}
{"tag": '中小学家长专区', "name": '青 春 期', "detail": '亲情港湾'}
{"tag": '大学生考试', "name": '考研', "detail": '考研英语'}
{"tag": '大学生考试', "name": '考研', "detail": '考研数学'}
{"tag": '大学生考试', "name": '考研', "detail": '考研政治'}
{"tag": '大学生考试', "name": '考研', "detail": '专业课'}
{"tag": '大学生考试', "name": '考研', "detail": '复试/调剂'}
{"tag": '大学生考试', "name": '四 六 级', "detail": 'CET-4'}
{"tag": '大学生考试', "name": '四 六 级', "detail": 'CET-6'}
{"tag": '大学生考试', "name": '等级考试', "detail": '计算机二级'}
{"tag": '大学生考试', "name": '等级考试', "detail": '计算机三级'}
{"tag": '出国留学', "name": '留学考试', "detail": '雅思'}
{"tag": '出国留学', "name": '留学考试', "detail": '托福'}
{"tag": '出国留学', "name": '留学考试', "detail": 'GRE'}
{"tag": '出国留学', "name": '留学考试', "detail": 'SAT'}
{"tag": '出国留学', "name": '留学考试', "detail": 'SSAT'}
{"tag": '出国留学', "name": '留学考试', "detail": 'GMAT'}
{"tag": '出国留学', "name": '留学考试', "detail": 'AP'}
{"tag": '出国留学', "name": '留学技巧', "detail": '留学面试'}
{"tag": '出国留学', "name": '留学技巧', "detail": '留学申请'}
{"tag": '出国留学', "name": '留学技巧', "detail": '留学择校'}
{"tag": '出国留学', "name": '留学技巧', "detail": '留学签证'}
{"tag": '出国留学', "name": '留学指导', "detail": '澳洲留学'}
{"tag": '出国留学', "name": '留学指导', "detail": '亚洲留学'}
{"tag": '出国留学', "name": '留学指导', "detail": '欧洲留学'}
{"tag": '出国留学', "name": '留学指导', "detail": '美洲留学'}
{"tag": '文化/生活/兴趣', "name": '生活技巧', "detail": '美食'}
{"tag": '文化/生活/兴趣', "name": '生活技巧', "detail": '化妆'}
{"tag": '文化/生活/兴趣', "name": '生活技巧', "detail": '服饰'}
{"tag": '文化/生活/兴趣', "name": '生活技巧', "detail": '购物'}
{"tag": '文化/生活/兴趣', "name": '生活技巧', "detail": '婚恋讲堂'}
{"tag": '文化/生活/兴趣', "name": '生活技巧', "detail": '生存逃生'}
{"tag": '文化/生活/兴趣', "name": '生活技巧', "detail": '孕妇培训'}
{"tag": '文化/生活/兴趣', "name": '生活技巧', "detail": '社交礼仪'}
{"tag": '文化/生活/兴趣', "name": '生活技巧', "detail": '其它'}
{"tag": '文化/生活/兴趣', "name": '文化艺术', "detail": '国学'}
{"tag": '文化/生活/兴趣', "name": '文化艺术', "detail": '文学'}
{"tag": '文化/生活/兴趣', "name": '文化艺术', "detail": '美术/绘画'}
{"tag": '文化/生活/兴趣', "name": '文化艺术', "detail": '书法'}
{"tag": '文化/生活/兴趣', "name": '文化艺术', "detail": '乐器/乐理'}
{"tag": '文化/生活/兴趣', "name": '文化艺术', "detail": '音乐'}
{"tag": '文化/生活/兴趣', "name": '文化艺术', "detail": '影视'}
{"tag": '文化/生活/兴趣', "name": '文化艺术', "detail": '其它'}
{"tag": '文化/生活/兴趣', "name": '兴趣爱好', "detail": '摄影'}
{"tag": '文化/生活/兴趣', "name": '兴趣爱好', "detail": '旅游'}
{"tag": '文化/生活/兴趣', "name": '兴趣爱好', "detail": '星座'}
{"tag": '文化/生活/兴趣', "name": '兴趣爱好', "detail": '塔罗牌'}
{"tag": '文化/生活/兴趣', "name": '兴趣爱好', "detail": '动漫'}
{"tag": '文化/生活/兴趣', "name": '兴趣爱好', "detail": '围棋'}
{"tag": '文化/生活/兴趣', "name": '兴趣爱好', "detail": '象棋'}
{"tag": '文化/生活/兴趣', "name": '兴趣爱好', "detail": '游戏'}
{"tag": '文化/生活/兴趣', "name": '兴趣爱好', "detail": '健身'}
{"tag": '文化/生活/兴趣', "name": '兴趣爱好', "detail": '瑜伽'}
{"tag": '文化/生活/兴趣', "name": '兴趣爱好', "detail": '羽毛球'}
{"tag": '文化/生活/兴趣', "name": '兴趣爱好', "detail": '舞蹈'}
{"tag": '文化/生活/兴趣', "name": '兴趣爱好', "detail": '汽车'}
{"tag": '文化/生活/兴趣', "name": '兴趣爱好', "detail": '手工DIY'}
{"tag": '文化/生活/兴趣', "name": '兴趣爱好', "detail": '其他'}
{"tag": '公开课学术学科', "name": 'TED课程', "detail": '综合'}
{"tag": '公开课学术学科', "name": 'TED课程', "detail": '理工'}
{"tag": '公开课学术学科', "name": 'TED课程', "detail": '艺术'}
{"tag": '公开课学术学科', "name": 'TED课程', "detail": '趣味'}
{"tag": '公开课学术学科', "name": 'TED课程', "detail": '传媒'}
{"tag": '公开课学术学科', "name": 'TED课程', "detail": '历史'}
{"tag": '公开课学术学科', "name": 'TED课程', "detail": '心理'}
{"tag": '公开课学术学科', "name": 'TED课程', "detail": '社会'}
{"tag": '公开课学术学科', "name": 'TED课程', "detail": '科技'}
{"tag": '公开课学术学科', "name": '名校课程', "detail": '综合'}
{"tag": '公开课学术学科', "name": '名校课程', "detail": '趣味'}
{"tag": '公开课学术学科', "name": '名校课程', "detail": '历史'}
{"tag": '公开课学术学科', "name": '名校课程', "detail": '经管'}
{"tag": '公开课学术学科', "name": '名校课程', "detail": '文艺'}
{"tag": '公开课学术学科', "name": '名校课程', "detail": '理工'}
{"tag": '公开课学术学科', "name": '名校课程', "detail": '传媒'}
{"tag": '公开课学术学科', "name": '名校课程', "detail": '心理'}
{"tag": '公开课学术学科', "name": '名校课程', "detail": '社会'}
{"tag": '公开课学术学科', "name": '社会科学', "detail": '历史'}
{"tag": '公开课学术学科', "name": '社会科学', "detail": '心理学'}
{"tag": '公开课学术学科', "name": '社会科学', "detail": '宗教'}
{"tag": '公开课学术学科', "name": '社会科学', "detail": '经济学'}
{"tag": '公开课学术学科', "name": '社会科学', "detail": '新闻/传媒'}
{"tag": '公开课学术学科', "name": '形式科学', "detail": '数学'}
{"tag": '公开课学术学科', "name": '形式科学', "detail": '数理逻辑'}
{"tag": '公开课学术学科', "name": '形式科学', "detail": '计算机科学'}
{"tag": '公开课学术学科', "name": '自然科学', "detail": '自然地理学'}
{"tag": '公开课学术学科', "name": '自然科学', "detail": '天文学'}
{"tag": '公开课学术学科', "name": '自然科学', "detail": '风水学'}
{"tag": '公开课学术学科', "name": '自然科学', "detail": '化学'}
{"tag": '公开课学术学科', "name": '自然科学', "detail": '物理学'}
{"tag": '公开课学术学科', "name": '自然科学', "detail": '生物学'}
{"tag": '公开课学术学科', "name": '应用科学', "detail": '运筹学'}
{"tag": '公开课学术学科', "name": '应用科学', "detail": '土木工程'}
{"tag": '公开课学术学科', "name": '应用科学', "detail": '软件工程'}
"""

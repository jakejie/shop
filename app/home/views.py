from flask import render_template, flash, session, redirect, request, url_for
from . import home
from app.model import TagList, Tags, Tag, Goods, User, UserLog, Comment, Address, \
    Orders, Count, Collect, Detail
from app import db
from app.home.form import LoginForm, RegistForm, UserDetailForm, CommentForm
from werkzeug.security import generate_password_hash
from functools import wraps
import uuid, os, datetime
from flask_login import login_required, logout_user, login_user
# 获取当前登录用户对象
from flask_login import current_user


# 轮播图嵌套页面 传递5个热门资源作为参数
@home.route('/animation')
def animation():
    return render_template('home/animation.html')


# 首页 分类列表页 一级
@home.route('/')
def index():
    tag_list = TagList.query.all()
    tags = Tags.query.all()
    tag = Tag.query.all()
    shops = Goods.query.all()
    return render_template('home/index.html', tag_list=tag_list,
                           shops=shops, tags=tags, tag=tag)


# 分类列表页 二级
@home.route('/tag=<int:tag>')
def tag(tag):
    name = TagList.query.filter_by(id=tag).first()
    tags = Tags.query.filter_by(f_name=name.name).all()
    tag = Tag.query.filter_by(t_name=tags[0].name).first()
    shops = Goods.query.filter_by(good_tag=tag.name).all()
    return render_template('home/tag.html', title=name.name,
                           shops=shops, tags=tags, Tag=Tag)


# 分类列表页 三级
@home.route('/tag=<int:tag>/tags=<int:tags>')
def theree_tag(tag, tags):
    info = Tag.query.filter_by(id=tags).first()  # 根据该标签 查找改标签的中文名字
    shop = Goods.query.filter_by(good_tag=info.name).all()  # 该分类下的商品信息
    return render_template('home/tag.html', title=info.name, shops=shop)


# 详情页
@home.route('/detail/goods=<string:goods_id>')
def detail(goods_id):
    info = Goods.query.filter_by(id=goods_id).first()
    comments = Comment.query.filter_by(comment_good_id=goods_id).all()  # 该商品评论信息
    who_buy = Detail.query.filter_by(goods_id=goods_id).all()  # 谁购买过该商品
    who_col = Collect.query.filter_by(good_id=goods_id).all()  # 谁收藏过该商品
    return render_template('home/detail.html', title=info.name, comments=comments,
                           buys=who_buy, cols=who_col, info=info)


# 结算页
@home.route('/pay/<int:order_id>')
@login_required
def pay(order_id=None):
    return ""


# 搜索页
@home.route('/search')
def search():
    return ""


# 登录页=ok
@home.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(username=data['username']).first()
        if not user.check_pwd(data['password']):
            flash('密码错误', 'err')
            return redirect(url_for('home.login'))
        session['user'] = user.username
        session['user_id'] = user.id
        # 记录用户的登录状态
        login_user(user, True)
        """
        login_user函数的第一个参数是需要登录的用户对象，
        第二个参数是bool值，如果为False，
        那么关闭浏览器后用户会话就会中断，
        下次用户访问时需要重新登录。
        如果为True，那么会在浏览器中写入一个长期有效的cookie，
        使用该cookie可以复原用户会话。
        """
        # userlog = UserLog(
        #     user=user.username,
        #     ip_add=request.remote_addr
        # )
        # db.session.add(userlog)
        # db.session.commit()
        return redirect(url_for('home.user'))
    return render_template("home/login.html", form=form)


# 注册页=ok
@home.route('/register', methods=["POST", "GET"])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            username=data['username'],
            email=data['email'],
            phone=data['phone'],
            password=generate_password_hash(data['password']),
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash('注册成功', 'ok')
        # 注册成功后 跳转到登陆页面
        return redirect(url_for('home.login'))
    return render_template('home/register.html', form=form)


# 退出登陆=ok
@home.route('/logout')
@login_required
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    logout_user()
    return redirect(url_for("home.login"))


# 个人中心
@home.route('/user')
@login_required
def user():
    form = UserDetailForm()
    uuid = current_user.id
    if uuid == None or uuid == "":
        return redirect(url_for('home.login'))
    user = User.query.filter_by(id=uuid).first()
    # GET方法 获取个人信息数据
    if request.method == 'GET':
        user = User.query.filter_by(id=uuid).first()
        return render_template('home/user.html', user=user, form=form)
    # POST方法 修改个人信息
    if form.validate_on_submit():
        data = form.data
        name_count = User.query.filter_by(name=data['name']).count()
        if data['name'] != user.name and name_count == 1:
            flash('昵称已经存在', 'err')
            return redirect(url_for('home.user'))

        phone_count = User.query.filter_by(phone=data['phone']).count()
        if data['phone'] != user.phone and phone_count == 1:
            flash('手机号码已经存在', 'err')
            return redirect(url_for('home.user'))

        email_count = User.query.filter_by(email=data['email']).count()
        if data['email'] != user.email and email_count == 1:
            flash('邮箱已经存在', 'err')
            return redirect(url_for('home.user'))

        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']
        db.session.add(user)
        db.session.commit()
        flash('修改成功', 'ok')
        return redirect(url_for('home.user'))


# 评论记录
@home.route('/comment')
@login_required
def comment():
    username = current_user.username
    comments = Comment.query.filter_by(users=username).all()
    return render_template('home/comment.html', comments=comments)


# 查看登陆日志
@home.route('/log')
@login_required
def log():
    username = current_user.username
    logs = UserLog.query.filter_by(user_logs=username).all()
    return render_template('home/logs.html', logs=logs)


# 查看收货地址
@home.route('/address')
@login_required
def address():
    username = current_user.username
    addres = Address.query.filter_by(users=username).all()
    return render_template('home/address.html', addres=addres)


# 购物车页
@home.route('/buy')
@login_required
def buy():
    username = current_user.username
    buy_s = Address.query.filter_by(users=username).all()
    return render_template('home/buy.html', buys=buy_s)


# 订单详情页==对商品添加评论=ok
@home.route('/order/<int:order_id>', methods=["POST", "GET"])
@login_required
def order_detail(order_id=None):
    form = CommentForm()
    if order_id == None:
        return redirect('home.order_list')
    username = current_user.username
    if request.method == "GET":
        info = Orders.query.filter_by(orderId=order_id, user=username).first()
        goods = Detail.query.filter_by(order_id=order_id).all()
        return render_template('home/order_detail.html', info=info, goods=goods)
    if form.validate_on_submit():
        data = form.data
        content = data['content']
        comment_good_id = data['comment_good_id']
        com = Comment(
            content=content,
            comment_good_id=comment_good_id,
            users=username,
        )
        db.session.add(com)
        db.session.commit()
        # 提交评论之后 继续展示该订单信息
        info = Orders.query.filter_by(orderId=order_id, user=username).first()
        goods = Detail.query.filter_by(order_id=order_id).all()
        return render_template('home/order_detail.html', info=info, goods=goods)


# 我的订单
@home.route('/order_list')
@login_required
def order_list():
    username = current_user.username
    orders = Orders.query.filter_by(user=username).all()
    return render_template('home/order_list.html', orders=orders, Detail=Detail)


# 收藏商品列表
@home.route('/collect')
@login_required
def collect():
    username = current_user.username
    collects = Collect.query.filter_by(users=username).all()
    return render_template('home/collect.html', collects=collects)


# 联系我们
@home.route('/connect')
def connect():
    return "联系我们"


# 帮助中心
@home.route('/help')
def help():
    return "帮助中心"


# 关于我们
@home.route('/about')
def about():
    return "关于我们"


# 购物流程介绍
@home.route('/buytip')
def how_to_buy():
    return "介绍"


# 常见问题
@home.route('/question')
def question():
    return "常见问题"


# 取消订单
@home.route('/cancel')
@login_required
def cancel_order():
    return "取消订单"


# 售后服务
@home.route('/service')
def service():
    return "售后服务"


# 网站导航
@home.route('/map')
def map():
    return "网站地图"


# 修改密码页面
@home.route('/pwd')
@login_required
def change_pwd():
    return "修改密码"

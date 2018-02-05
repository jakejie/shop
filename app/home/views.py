from flask import render_template, flash, session, redirect, request, \
    url_for, current_app
from . import home
from app.model import TagList, Tags, Tag, Course, User, UserLog, Comment, Address, \
    Orders, Collect, Detail, BuyCar
from app import db
from app.home.form import UserDetailForm, CommentForm
import uuid, os, datetime
from flask_login import login_required
# 获取当前登录用户对象
from flask_login import current_user


# 首页 分类列表页 一级
@home.route('/')
def index():
    return render_template('home/index.html')


# 所有课程
@home.route('/course/')
def course_list():
    return render_template('home/course-list.html')


# 所有授课教师
@home.route('/teachers/')
def teacher_list():
    return render_template('home/teachers-list.html')


# 授课教师详情页
@home.route('/teacher/<int:teacher_id>')
def teacher_detail(teacher_id=None):
    return render_template('home/teacher-detail.html')


# 所有机构
@home.route('/school/')
def school_list():
    return render_template('home/org-list.html')


# 课程详情页
@home.route('/detail/<int:course_id>')
def course_detail(course_id=None):
    return render_template('home/course-detail.html')


# 机构主页=首页
@home.route('/organization/home/<int:org_id>/')
def ori_homepage(org_id=None):
    return render_template('home/org-detail-homepage.html')


# 机构主页=课程
@home.route('/organization/course/<int:org_id>')
def ori_course(org_id=None):
    return render_template('home/org-detail-course.html')


# 机构主页==介绍
@home.route('/organization/desc/<int:org_id>')
def ori_desc(org_id=None):
    return render_template('home/org-detail-desc.html')


# 机构主页==讲师
@home.route('/organization/teacher/<int:org_id>')
def ori_teacher(org_id=None):
    return render_template('home/org-detail-teachers.html')


@home.route('/user', methods=["POST", "GET"])
@login_required
def user():
    if current_user.id == None or current_user.id == "":
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(id=current_user.id).first()
    form = UserDetailForm(info=user.info)
    # GET方法 获取个人信息数据
    if request.method == 'GET':
        return render_template('home/usercenter-info.html', user=user, form=form)
    # POST方法 修改个人信息
    if form.validate_on_submit():
        file = form.image.data
        filename = user.username + '-' + file.filename.replace(' ', '').replace('/', '').replace('\\', '')
        file.save('app/static/image/user/' + filename)
        user.info = form.data.get("info")
        user.image = filename
        db.session.add(user)
        db.session.commit()
        flash('修改成功', 'ok')
        return redirect(url_for('home.user'))
    flash("修改失败！ 简介不能为空")
    return render_template('home/usercenter-info.html', user=user, form=form)


# 购买过的课程
@home.route('/mycourse/')
@login_required
def mycourse():
    return render_template('home/usercenter-mycourse.html')


# 收到的消息
@home.route('/mymessage/')
@login_required
def mymessage():
    return render_template('home/usercenter-message.html')


# 收藏的所有
@home.route('/mycollect/')
@login_required
def mycollect():
    return render_template('home/usercenter-fav-course.html')


# 收藏的老师
@home.route('/collect_school/')
@login_required
def collect_teacher():
    return render_template('home/usercenter-fav-teacher.html')


# 收藏的机构
@home.route('/collect_teacher/')
@login_required
def collect_school():
    return render_template('home/usercenter-fav-org.html')


# 收藏的课程
@home.route('/collect_course/')
@login_required
def collect_course():
    return render_template('home/usercenter-fav-course.html')


# 评论记录
@home.route('/comment/')
@login_required
def comment():
    comments = Comment.query.filter_by(users=current_user.id).all()
    return render_template('home/user_comment.html', comments=comments)


# 查看登陆日志
@home.route('/userlog/')
@login_required
def user_log():
    logs = UserLog.query.filter_by(user_logs=current_user.id).all()
    return render_template('home/user_logs.html', logs=logs)


# 轮播图嵌套页面 传递5个热门资源作为参数
# @home.route('/animation')
# def animation():
#     return render_template('home/animation.html')

# tag_list = TagList.query.all()
# tags = Tags.query.all()
# tag = Tag.query.all()
# shops = Course.query.all()
# return render_template('home/index.html', tag_list=tag_list,
#                        shops=shops, tags=tags, tag=tag)


# 分类列表页 二级
# @home.route('/tag=<int:tag>')
# def tag(tag):
#     name = TagList.query.filter_by(id=tag).first()
#     tags = Tags.query.filter_by(f_name=name.name).all()
#     tag = Tag.query.filter_by(t_name=tags[0].name).first()
#     shops = Course.query.filter_by(good_tag=tag.name).all()
#     return render_template('home/tag.html', title=name.name,
#                            shops=shops, tags=tags, Tag=Tag)


# 分类列表页 三级
# @home.route('/tag=<int:tag>/tags=<int:tags>')
# def theree_tag(tag, tags):
#     info = Tag.query.filter_by(id=tags).first()  # 根据该标签 查找改标签的中文名字
#     shop = Course.query.filter_by(good_tag=info.name).all()  # 该分类下的商品信息
#     return render_template('home/tag.html', title=info.name, shops=shop)


# @home.route('/detail/goods=<string:goods_id>')
# def detail(goods_id):
#     info = Course.query.filter_by(good_id=goods_id).first()
#     comments = Comment.query.filter_by(comment_good_id=goods_id).all()  # 该商品评论信息
#     who_buy = Detail.query.filter_by(goods_id=goods_id).all()  # 谁购买过该商品
#     who_col = Collect.query.filter_by(good_id=goods_id).all()  # 谁收藏过该商品
#     if info == None:
#         return render_template('home/detail.html', info=info)
#     return render_template('home/detail.html', title=info.name, comments=comments,
#                            buys=who_buy, cols=who_col, info=info)


# # 结算页
# @home.route('/pay/<int:order_id>')
# @login_required
# def pay(order_id=None):
#     return ""
#
#
# # 搜索页
# @home.route('/search')
# def search():
#     return ""


# 个人中心 修改图像 修改个人简介

# # 查看收货地址==分页完成
# @home.route('/address/')
# @login_required
# def address():
#     page = request.args.get('page', 1, type=int)
#     pagination = Address.query.filter_by(users_id=current_user.id). \
#         order_by(Address.id.desc()).paginate(
#         page, per_page=current_app.config['DATA_PER_PAGE'],
#         error_out=False)
#     address = pagination.items
#     return render_template('home/address.html', address=address,
#                            pagination=pagination, endpoint='home.address')


# ----需要ajax----
# 提交订单页面 也可以是购物车页面 生成订单号
# 购物车页 可以选择商品直接去结算 点击按钮 去结算 自动根据用户id+时间戳生成订单号
# @home.route('/buy/', methods=["POST", "GET"])
# @home.route('/refer', methods=["POST", "GET"])
# @login_required
# def buy():
#     buy_s = BuyCar.query.filter_by(user_car=current_user.id).all()
#     if request.method == "GET":
#         return render_template('home/buy.html', buys=buy_s)
#     if request.method == "POST":
#         print(request.args.get('name'))
#         print(request.get_json())
#         print(type(request.get_data()))
#         print("哈哈哈：{}".format(request.data))
#         return "成功加入购物车！！！！！"


# @home.route('/car/product=<int:good_id>/num=<string:num>/', methods=["POST"])
# @login_required
# def car(good_id, num):
#     # 判断用户是否在购物车中已经存在该商品
#     print("商品：{} 数量：{}".format(good_id, num))
#     return "加入购物车成功！"


# 查看订单详情页==并且可以对购买过的商品添加评论=ok
# @home.route('/order/<int:order_id>', methods=["POST", "GET"])
# @login_required
# def order_detail(order_id=None):
#     form = CommentForm()
#     if order_id == None:
#         return redirect('home.order_list')
#     if request.method == "GET":
#         info = Orders.query.filter_by(order_id=order_id, user=current_user.id).first()
#         goods = Detail.query.filter_by(orderId=order_id).all()
#         return render_template('home/order_detail.html', info=info, goods=goods)
#     if form.validate_on_submit():
#         data = form.data
#         content = data['content']
#         comment_good_id = data['comment_good_id']
#         com = Comment(
#             content=content,
#             comment_good_id=comment_good_id,
#             users=current_user.id,
#         )
#         db.session.add(com)
#         db.session.commit()
#         # 提交评论之后 继续展示该订单信息
#         info = Orders.query.filter_by(order_id=order_id, user=current_user.id).first()
#         goods = Detail.query.filter_by(orderId=order_id).all()
#         return render_template('home/order_detail.html', info=info, goods=goods)


# 我的订单 查看所有的历史订单信息
# @home.route('/order_list/')
# @home.route('/order/')
# @login_required
# def order_list():
#     orders = Orders.query.filter_by(user=current_user.id).all()
#     return render_template('home/order_list.html', orders=orders)
#

# 收藏商品列表 查看所有收藏过的商品 以及 点击收藏之后 接收post请求 收藏
# @home.route('/collect', methods=["POST", "GET"])
# @login_required
# def collect():
#     collects = Collect.query.filter_by(users=current_user.id).all()
#     if request.method == "GET":
#         return render_template('home/collect.html', collects=collects)
#     else:
#         good_id = request.form.get('goods_id')
#         goods = request.form.get('goods')
#         inf = Collect(
#             users=current_user.id,
#             good_id=good_id,
#             goods=goods,
#         )
#         db.session.add(inf)
#         db.session.commit()
#         flash("收藏成功 可以在收藏列表查看所有收藏的商品")


# --------------------------静态固定页面----------------------------------#
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

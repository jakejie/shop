from flask import render_template, flash, session, redirect, request, \
    url_for, current_app, jsonify
from . import home
from app.model import TagList, Tags, Tag, Course, User, UserLog, Comment, Address, \
    Orders, Collect, Detail, BuyCar, School, Teacher, Message
from app import db
from app.home.form import UserDetailForm, CommentForm, PwdForm
import uuid, os, datetime, json, time
from flask_login import login_required
# 获取当前登录用户对象
from flask_login import current_user
from werkzeug.security import generate_password_hash


# 首页 推荐课程 推荐机构/学校 ok
@home.route('/')
def index():
    course = Course.query.limit(8)
    school = School.query.limit(15)
    return render_template('home/index.html',
                           course=course,
                           school=school)


# 所有课程 ok
@home.route('/course/<int:page>/')
def course_list(page=None):
    if page is None:
        page = 1
    pagination = Course.query.paginate(page=page, per_page=current_app.config['DATA_PER_PAGE'],
                                       error_out=False)
    course = pagination.items
    return render_template('home/course-list.html',
                           pagination=pagination,
                           endpoint='.course_list',
                           course=course)


# 所有授课教师 ok
@home.route('/teachers/<int:page>/')
def teacher_list(page=None):
    pagination = Teacher.query.paginate(page=page, per_page=current_app.config['DATA_PER_PAGE'],
                                        error_out=False)
    return render_template('home/teachers-list.html',
                           pagination=pagination,
                           endpoint='.teacher_list')


# 授课教师详情页 ok
@home.route('/teacher/<int:teacher_id>/')
def teacher_detail(teacher_id=None):
    teacher_info = Teacher.query.filter_by(id=teacher_id).first()
    course = Course.query.filter_by(teacher_name=teacher_info.teacher_name).all()
    school = School.query.filter_by(school_name=teacher_info.teacher_company).first()
    return render_template('home/teacher-detail.html',
                           teacher_info=teacher_info,
                           course=course,
                           school=school)


# 所有机构 ok
@home.route('/school/<int:page>/')
def school_list(page=None):
    pagination = School.query.paginate(page=page,
                                       per_page=current_app.config['DATA_PER_PAGE'],
                                       error_out=False)
    return render_template('home/org-list.html',
                           pagination=pagination,
                           endpoint='.school_list')


# 课程详情页=ok
@home.route('/detail/<int:course_id>')
def course_detail(course_id=None):
    info = Course.query.filter_by(course_id=course_id).first()
    teacher = Teacher.query.filter_by(teacher_name=info.teacher_name).first()
    school = School.query.filter_by(school_name=teacher.teacher_company).first()
    return render_template('home/course-detail.html', info=info,
                           teacher=teacher, school=school)


# 个人中心主页====无法修改数据
@home.route('/user/', methods=["POST", "GET"])
@login_required
def user():
    if current_user.id == None or current_user.id == "":
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(id=current_user.id).first()
    form = UserDetailForm()
    # GET方法 获取个人信息数据
    if request.method == 'GET':
        return render_template('home/usercenter-info.html', user=user, form=form)
    # POST方法 修改个人信息
    if form.validate_on_submit():
        print("获取到了数据了啊")
        # file = form.image.data
        # filename = user.username + '-' + file.filename.replace(' ', '').replace('/', '').replace('\\', '')
        # file.save('app/static/image/user/' + filename)
        # user.image = filename
        # 获取修改后的信息
        user.username = form.data.get("name")
        user.birthday = form.data.get("birthday")
        user.sex = form.data.get("sex")
        user.phone = form.data.get("phone")
        user.email = form.data.get("email")
        user.info = form.data.get("info")

        db.session.add(user)
        db.session.commit()
        flash('修改成功', 'ok')
        return redirect(url_for('home.user'))
    flash("修改失败！ 简介不能为空")
    return render_template('home/usercenter-info.html', user=user, form=form)


# 修改密码界面
@home.route('/pwd/', methods=['GET', 'POST'])
@login_required
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session['user']).first()  # 查找账号
        if not user.check_pwd(data['old_pwd']):
            flash("旧密码错误", "err")
            return redirect(url_for('home.pwd'))
        user.pwd = generate_password_hash(data['new_pwd'])
        db.session.add(user)
        db.session.commit()
        flash("修改成功,请重新登录", "ok")
        return redirect(url_for('home.logout'))
    return render_template("home/pwd.html", form=form)


@home.route('/buy/<int:page>')
@login_required
def buy(page=None):
    pagination = BuyCar.query.filter_by(user_car=current_user.id). \
        paginate(page=page, per_page=current_app.config['DATA_PER_PAGE'], error_out=False)
    buycar = pagination.items
    return render_template('home/user_buys.html',
                           pagination=pagination,
                           endpoint='.buy',
                           buycar=buycar)


# 购买过的课程 ok
@home.route('/mycourse/')
@login_required
def mycourse():
    course = Detail.query.filter_by(user=current_user.id).all()
    return render_template('home/usercenter-mycourse.html', course=course)


# 收到的消息/通知 ok
@home.route('/mymessage/')
@login_required
def mymessage():
    message = Message.query.filter_by(user_mess=current_user.id).all()
    return render_template('home/usercenter-message.html', messages=message)


# 收藏的课程 ok
@home.route('/mycollect/')
@login_required
def mycollect():
    col_course = Collect.query.filter_by(users=current_user.id, col_type=1).all()
    return render_template('home/usercenter-fav-course.html', col_course=col_course)


# 收藏的老师 ok
@home.route('/collect_school/')
@login_required
def collect_teacher():
    teacher = Collect.query.filter_by(users=current_user.id, col_type=3).all()
    return render_template('home/usercenter-fav-teacher.html', teacher=teacher)


# 收藏的机构/学校 ok
@home.route('/collect_teacher/')
@login_required
def collect_school():
    school = Collect.query.filter_by(users=current_user.id, col_type=2).all()
    return render_template('home/usercenter-fav-org.html', school=school)


# 评论记录 ok
@home.route('/comment/')
@login_required
def comment():
    comments = Comment.query.filter_by(users=current_user.id).all()
    return render_template('home/user_comment.html', comments=comments)


# 查看登陆日志 ok
@home.route('/userlog/')
@login_required
def user_log():
    logs = UserLog.query.filter_by(user_logs=current_user.id).all()
    return render_template('home/user_logs.html', user_log=logs)


# 添加收藏数据 ok
@home.route('/org/add_fav/', methods=["POST"])
@login_required
def add_fav():
    try:
        user_id = current_user.id
        # 将获取到的数据写入到数据库
        data = json.loads(request.data)
        fav_id = data["fav_id"]
        fav_type = data["fav_type"]
        # 查询是否已经收藏过
        result = Collect.query.filter_by(col_type=fav_type, course_id=fav_id, users=user_id).count()
        if result == 0:
            info = Collect(
                col_type=fav_type,
                course_id=fav_id,
                users=user_id,
            )
            db.session.add(info)
            db.session.commit()
            return jsonify({"status": "success",
                            "msg": "收藏成功啦",
                            })
        else:
            return jsonify({"status": "success",
                            "msg": "您已经收藏过啦",
                            })
    except Exception as e:
        return jsonify({"status": "fail",
                        "msg": "收藏错误：{}".format(e)
                        })


# 删除收藏数据 ok
@home.route('/org/del_fav/', methods=["POST"])
@login_required
def del_fav():
    try:
        user_id = current_user.id
        # 将获取到的数据写入到数据库
        data = json.loads(request.data)
        fav_id = data["fav_id"]
        fav_type = data["fav_type"]
        info = Collect.query.filter_by(
            users=user_id,
            col_type=fav_type,
            course_id=fav_id
        ).first()
        db.session.delete(info)
        db.session.commit()
        return jsonify({"status": "success",
                        "msg": "删除成功",
                        })
    except Exception as e:
        return jsonify({"status": "fail",
                        "msg": "删除失败：{}".format(e)
                        })


# 添加到购物车数据 ok
@home.route('/org/add_car/', methods=["POST"])
@login_required
def add_car():
    try:
        user_id = current_user.id
        data = json.loads(request.data)
        fav_id = data["fav_id"]
        price = data["price"]
        # 查询是否已经添加过购物车
        result = BuyCar.query.filter_by(course_id=fav_id, user_car=user_id).count()
        if result == 0:
            info = BuyCar(
                price=price,
                course_id=fav_id,
                user_car=user_id,
            )
            db.session.add(info)
            db.session.commit()
            return jsonify({"status": "success",
                            "msg": "成功加入购物车啦",
                            })
        else:
            return jsonify({"status": "success",
                            "msg": "该商品已经在您的购物车啦",
                            })
    except Exception as e:
        return jsonify({"status": "fail",
                        "msg": "用户未登录"
                        })


# 删除购物车的商品数据
@home.route('/org/del_car/', methods=["POST"])
@login_required
def del_car():
    try:
        user_id = current_user.id
        data = json.loads(request.data)
        fav_id = data["course_id"]
        info = BuyCar.query.filter_by(
            course_id=fav_id, user_car=user_id
        ).first()
        db.session.delete(info)
        db.session.commit()
        return jsonify({"status": "success",
                        "msg": "删除成功",
                        })
    except Exception as e:
        return jsonify({"status": "fail",
                        "msg": "删除失败：{}".format(e)
                        })


# 接受需要结算的商品列表 写入数据表 生成订单号
@home.route('/cart/clearing', methods=["POST"])
@login_required
def cart_clearing():
    data = json.loads(request.data)
    add_time = int(time.time())
    # 提交订单之前 确认之前是否购买过该课程
    buy_or = Detail.query.filter_by(
        course_id=data["cid"],
        user=current_user.id
    ).count()
    # 购买过该商品
    if buy_or == 1:
        return jsonify({"status": "fail",
                        "msg": "您已经购买过该商品啦!"})
    # 没有购买过 进行订单结算并从购物车移除 等操作
    else:
        result = Orders.query.filter_by(user=current_user.id, order_id=add_time).count()
        if result == 1:
            pass
            # print(result)
            # 直接使用该订单号 写入其他商品
        else:
            # 写入订单号
            info = Orders(
                order_id=add_time,
                address=current_user.email,
                user=current_user.id,
                times=add_time,
                add_time=datetime.datetime.now()
            )
            db.session.add(info)
            db.session.commit()
        # 写入商品到detail
        det = Detail(
            add_time=datetime.datetime.now(),
            course_id=data["cid"],
            num=data["cnum"],
            orderId=add_time,
            user=current_user.id,
            price=Course.query.filter_by(course_id=data["cid"]).first().price,
        )
        db.session.add(det)
        db.session.commit()
        # 成功提交订单之后 将商品从购物车中删除
        cart = BuyCar.query.filter_by(course_id=data["cid"], user_car=current_user.id).first()
        db.session.delete(cart)
        db.session.commit()
        return jsonify({"status": "success",
                        "msg": "订单提交成功 去支付吧!"})


# 待支付订单中心 所有待支付订单
@home.route('/cart/waitpay/', methods=["POST", "GET"])
@login_required
def wait_pay():
    if request.method == "GET":
        return "待支付中心"
    else:
        print("取消该订单的支付")


# 购物车结算中心
@home.route('/buy/cart/')
@login_required
def buy_cart():
    # 先查询数据表 是否存在多个待支付订单
    # 先处理已经存在的待支付订单
    orde = Orders.query.filter_by(pay=0, cancel=0, user=current_user.id).count()
    if orde > 1:
        print("有多个订单没有支付哦")
        return render_template('home/user-wait-pay.html')
    # 取出唯一待支付订单 进行支付
    order_id = Orders.query.filter_by(user=current_user.id, pay=0, cancel=0).first()
    money = 0
    for price in Detail.query.filter_by(orderId=order_id.order_id).all():
        money = float(money) + float(price.price)
    return render_template('home/user-pay.html', money=money)


# 机构主页=首页 ok
@home.route('/organization/home/<int:org_id>/')
def ori_homepage(org_id=None):
    school = School.query.filter_by(id=org_id).first()
    course = Course.query.filter_by(school_id=school.id).all()
    return render_template('home/org-detail-homepage.html',
                           school=school,
                           course=course)


# 机构主页=课程 ok
@home.route('/organization/course/<int:org_id>')
def ori_course(org_id=None):
    school = School.query.filter_by(id=org_id).first()
    course = Course.query.filter_by(school_id=school.id).all()
    return render_template('home/org-detail-course.html',
                           school=school, course=course)


# 机构主页==介绍 ok
@home.route('/organization/desc/<int:org_id>')
def ori_desc(org_id=None):
    school = School.query.filter_by(id=org_id).first()
    return render_template('home/org-detail-desc.html',
                           school=school)


# 机构主页==讲师 ok
@home.route('/organization/teacher/<int:org_id>')
def ori_teacher(org_id=None):
    school = School.query.filter_by(id=org_id).first()
    teacher = Teacher.query.filter_by(teacher_company=school.school_name).all()
    return render_template('home/org-detail-teachers.html',
                           school=school, teacher=teacher)


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

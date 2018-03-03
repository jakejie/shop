from flask import render_template, flash, session, redirect, request, \
    url_for, current_app, jsonify
from . import home
from app.model import TagList, Tags, Tag, Course, User, UserLog, Comment, Address, \
    Orders, Collect, Detail, BuyCar, School, Teacher, Message
from app import db
from app.home.form import UserDetailForm, CommentForm, PwdForm, BuyCart
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
    form = UserDetailForm()

    user = User.query.filter_by(id=current_user.id).first()

    # POST方法 修改个人信息
    if form.validate_on_submit():
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
        db.session.commit()
        flash('修改成功', 'ok')
        return redirect(url_for('home.user'))

    else:
        # GET方法 获取个人信息数据
        return render_template('home/usercenter-info.html', user=user, form=form)


allowed_file = ['png', 'jpg']
# UPLOAD_FOLDER = os.path.abspath(os.path.pardir) + '/app/static/tmp/'
UPLOAD_FOLDER = r'C:\20180128\shop\app\static\media\image\2016\11'


# 修改个人图像 ok
@home.route('/users/image/upload/', methods=["POST", "GET"])
@login_required
def upload_image():
    if request.method == "POST":
        # print("上传图片啦")
        file = request.files['file']
        # print(file.filename)
        # if file.filename[-3] in allowed_file:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        file_name = 'media/image/2016/11/' + file.filename
        info = User.query.filter_by(id=current_user.id).first()
        info.image = file_name
        db.session.commit()
    return redirect(url_for('home.user'))


# 修改密码界面
@home.route('/change_pwd/', methods=['GET', 'POST'])
@login_required
def change_pwd():
    form = PwdForm()
    # if form.validate_on_submit():
    if request.method == "POST":
        print("提交了密码")
        data = form.data
        user = User.query.filter_by(id=current_user.id).first()  # 查找账号
        if not user.check_pwd(data['old_pwd']):
            flash("旧密码错误", "err")
            return redirect(url_for('home.change_pwd'))
        user.pwd = generate_password_hash(data['new_pwd'])
        # db.session.add(user)
        db.session.commit()
        flash("修改成功,请重新登录", "ok")
        return redirect(url_for('home.logout'))
    else:
        return render_template("home/user-change_pwd.html", form=form)


# 我的购物车页面 ok
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


# 购买过的课程/已支付课程 ok
@home.route('/mycourse/')
@login_required
def mycourse():
    course = Detail.query.filter_by(user=current_user.id).all()
    return render_template('home/usercenter-mycourse.html', course=course)


# 待支付订单中心 所有待支付订单 ok
@home.route('/cart/waitpay/', methods=["POST", "GET"])
@login_required
def wait_pay():
    if request.method == "GET":
        order = Orders.query.filter_by(user=current_user.id, pay=0, cancel=0).all()
        return render_template('home/user-wait-pay.html', order=order)
    else:
        print("取消该订单的支付")


# 已经取消订单的对应课程
@home.route('/cancel/', methods=["POST", "GET"])
@login_required
def cancel():
    if request.method == "GET":
        order = Orders.query.filter_by(user=current_user.id, cancel=1).all()
        return render_template('home/user-cancel.html', order=order)
    else:
        # 接收需要取消的订单的订单号 修改数据表的是否取消订单的标记
        pass


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


# 删除购物车的商品数据 ok
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


# 接受需要结算的商品列表 写入数据表 生成订单号 ok
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


# 购物车结算中心 ok
@home.route('/buy/cart/<int:order_id>', methods=["POST", "GET"])
@login_required
def buy_cart(order_id=None):
    form = BuyCart()
    if request.method == "GET":
        if order_id == 1:
            order_id = Orders.query.filter_by(user=current_user.id, pay=0, cancel=0).first().order_id
        return render_template('home/user-pay.html', form=form, order_id=order_id)

    if form.validate_on_submit():
        data = form.data
        info = Orders.query.filter_by(user=current_user.id, order_id=order_id).first()
        info.alipay = data["alipay"],
        info.pay_remark = data["remark"],
        info.pay = 1
        db.session.commit()
        return redirect(url_for('home.mycourse'))


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


# 售后服务
@home.route('/service')
def service():
    return "售后服务"


# 网站导航
@home.route('/map')
def map():
    return "网站地图"

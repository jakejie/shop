from . import admin
from app import db
from flask import render_template, flash, redirect, request, session, url_for
from flask_login import login_required, current_user
from app.model import Count, Course, Tag, Tags, TagList, Orders, \
    Collect, Comment, BuyCar, Detail, Address, User, UserLog
from .form import AddGoodsForm
import time


# 后台管理主页 显示统计数据
@admin.route('/')
@login_required
def index():
    username = current_user.username
    if username == "admin":
        info = Count.query.first()
        return render_template('admin/index.html', count=info)
    # 如果不是使用的管理员账号 跳转到商城主页
    else:
        tag_list = TagList.query.all()
        tags = Tags.query.all()
        tag = Tag.query.all()
        shops = Course.query.all()
        return render_template('home/index.html', tag_list=tag_list,
                               shops=shops, tags=tags, tag=tag)


# 商品添加页面 直接发布新商品 GET请求查看发布商品的页面 POST请求提交新数据
@admin.route('/add_goods/', methods=["POST", "GET"])
@login_required
def add_good():
    form = AddGoodsForm()
    username = current_user.username
    if request.method == "GET":
        if username != "admin":
            flash("该用户为普通用户")
            flash("请使用admin管理员账号登陆！")
            return redirect(url_for('auth.login'))
        else:
            return render_template('admin/add_goods.html', form=form)
    if form.validate_on_submit():
        # 商品主图 只能插入一张主图 封面图
        file = form.image.data
        filename = username + '-' + file.filename.replace(' ', '').replace('/', '').replace('\\', '')
        file.save('app/static/image/skull/' + filename)
        inf = Course(
            good_id=int(time.time()),  # 商品id
            name=form.name.data,  # 商品名称
            image=filename,  # 商品图片
            good_tag=form.good_tag.data,  # 商品标签
            chap_num=form.chap_num.data,  # 章节
            price=form.price.data,  # 价格
            old_price=form.old_price.data,
            start=form.start.data,
            discount=form.discount.data,
            course_info=form.info.data,
            target=form.target.data,
        )
        db.session.add(inf)
        db.session.commit()
        if form.target.data == 0:
            flash("该商品暂未上架 您可在待上架商品中查看", 'ok')
        if form.target.data == 1:
            flash("该商品上架成功", 'ok')
        return redirect('admin.add_good')
    return render_template('admin/add_goods.html', form=form)


# 富文本内容编辑 也就是商品详情编辑==暂时无法使用 有bug
@admin.route('/upload/', methods=['GET', 'POST'])
def upload():
    print(request.method)
    if request.method == "POST":
        print(request.get_data())
    pass


# 等待上架商品==编辑操作按钮(1：上架 2：删除)
@admin.route('/wait_goods/')
@login_required
def wait_goods():
    username = current_user.username
    if username != "admin":
        flash("请使用admin账号登陆")
        return redirect(url_for('auth.login'))
    else:
        product = Course.query.filter_by(target=0).all()
        return render_template('admin/wait_goods.html', goods=product)


# 将商品上架
@admin.route('/push/', methods=["POST"])
@login_required
def push():
    if request.method == "POST":
        goods_id = request.args.get("good_id")
        good = Course.query.filter_by(good_id=goods_id)
        good.target = 1
        db.session.add(good)
        db.session.commit()
        return "上架成功！"


# 将商品进行下架操作
@admin.route('/pull/')
@login_required
def pull():
    if request.method == "POST":
        goods_id = request.args.get("good_id")
        good = Course.query.filter_by(good_id=goods_id)
        good.target = 0
        db.session.add(good)
        db.session.commit()
        return "下架成功！"


# 将待上架的商品进行删除操作
@admin.route('/delete/', methods=["POST"])
def del_good():
    if request.method == "POST":
        goods_id = request.args.get("good_id")
        good = Course.query.filter_by(good_id=goods_id)
        db.session.delete(good)
        db.session.commit()
        return "删除成功！"


# 出售中商品==编辑操作按钮(1：下架 2：删除 3：编辑修改)
@admin.route('/wait_goods/')
@login_required
def sale_goods():
    username = current_user.username
    if username != "admin":
        flash("请使用admin账号登陆")
        return redirect(url_for('auth.login'))
    else:
        product = Course.query.filter_by(target=1).all()
        return render_template('admin/sale_goods.html', goods=product)


# 查看所有商品信息==包括上架的 未上架的
@admin.route('/goods')
@login_required
def goods_list():
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        product = Course.query.all()
        return render_template('admin/goods.html', goods=product)


# 商品编辑页面
@admin.route('/edit_goods')
@admin.route('/edit_goods/<int:goods_id>', methods=["POST", "GET"])
@login_required
def edit_good(goods_id=None):
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        if goods_id == None:
            return redirect(url_for('admin.goods_list'))
        else:
            if request.method == "GET":
                # 显示需要编辑的商品的信息
                info = Course.query.filter_by(good_id=goods_id).first()
                return render_template('admin/edit_goods.html', goods=info)
            else:
                # POST请求 也就是提交了修改后的商品数据
                product = Course.query.filter_by(good_id=goods_id).first()
                product.name = request.form["name"]  # 商品名称
                product.image = request.form["image"]  # 商品图片
                product.good_tag = request.form["good_tag"]  # 商品标签
                product.chap_num = request.form["chap_num"]  # 章节
                product.price = request.form["price"]  # 价格
                product.old_price = request.form["old_price"]  # 原价
                product.start = request.form["start"]  # 星级
                product.discount = request.form["discount"]  # 折扣
                product.course_info = request.form["course_info"]  # 简介
                product.target = request.form["target"]  # 是否上架
                db.session.add(product)
                db.session.commit()
                return redirect(url_for('admin.edit_good', goods_id=goods_id))


# 查看所有订单页面
# 修改订单页面==编辑操作按钮(1：修改订单 2：删除订单)
@admin.route('/orders/<int:order_id>')
@admin.route('/orders/')
@login_required
def orders(order_id=None):
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        if order_id == None:
            order = Orders.query.all()
            return render_template('admin/orders.html', order=order)
        else:
            info = Orders.query.filter_by(order_id=order_id).first()
            return render_template('admin/order_detail.html', info=info)


# 订单编辑 修改订单的地址 订单的商品数量 添加备注
@admin.route('/order/edit/<int:order_id>', methods=["POST"])
@login_required
def edit_order(order_id):
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        info = Orders.query.filter_by(order_id=order_id).first()
        return render_template('admin/edit_order.html', info=info)


# 订单删除
@admin.route('/order/del/', methods=["POST"])
@login_required
def del_order():
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        order_id = request.form["order_id"]
        info = Orders.query.filter_by(order_id=order_id).first()
        db.session.delete(info)
        detail = Detail.query.filter_by(orderId=order_id).first()
        db.session.delete(detail)
        db.session.commit()
        return "订单删除成功 刷新后订单消失！"


# 查看所有评论信息 编辑评论信息 修改评论 删除评论
@admin.route('/comments')
@admin.route('/comments/<int:comment_id>')
@login_required
def comments(comment_id=None):
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        if comment_id == None:
            # 展示所有评论数据
            com = Comment.query.all()
            return render_template('admin/comments.html', comment=com)
        else:
            # 查看评论详情==删除+编辑
            com = Comment.query.filter_by(id=comment_id).first()
            return render_template('admin/comment_detail.html', comment=com)


# 删除评论数据
@admin.route('/delete/comment/', methods=["POST"])
@login_required
def delete_comment():
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        comment_id = request.form["comment_id"]
        info = Comment.query.filter_by(id=comment_id).first()
        db.session.delete(info)
        db.session.commit()
        return "评论删除成功 刷新后消失"


# 编辑评论数据
@admin.route('/edit/comment/<int:comment_id>', methods=["POST", "GET"])
@login_required
def edit_comment(comment_id):
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        info = Comment.query.filter_by(id=comment_id).first()
        if request.method == "GET":
            info = Comment.query.filter_by(id=comment_id).first()
            return render_template('admin/comment_detail.html', comment=info)
        else:
            content = request.form["content"]
            info.content = content
            db.session.add(info)
            db.session.commit()
            return "评论修改成功"


# 查看所有会员信息==会员订单==购物车==收藏==评论
@admin.route('/vip')
@login_required
def vip():
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        user = User.query.all()
        return render_template('admin/vip.html', user=user)


# 编辑会员信息
@admin.route('/edit/vip/<int:user_id>', methods=["POST", "GET"])
@login_required
def edit_vip(user_id):
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        user = User.query.filter_by(id=user_id).first()
        if request.method == "GET":
            return render_template('admin/vip_edit.html', info=user)
        else:
            user.username = request.form["username"]
            user.email = request.form["email"]
            user.phone = request.form["phone"]
            db.session.add(user)
            db.session.commit()
            return "会员信息修改成功！"


# 会员订单
@admin.route('/vip/id=<int:user_id>')
@admin.route('/vip/order=/')
@login_required
def vip_order(user_id=None):
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        if user_id == None:
            # 没有指定用户id 查看所有用户的订单
            order = Orders.query.all()
            return render_template('admin/orders.html', order=order)
        else:
            # 根据用户id 查看对应该用户所有的历时订单
            order = Orders.query.filter_by(user=user_id).all()
            return render_template('admin/vip_order.html', order=order)


# 购物车
@admin.route('/vip/buy=<string:user_id>')
@admin.route('/vip/buy=/')
@login_required
def vip_buy(user_id=None):
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        if user_id == None:
            car = BuyCar.query.all()
            return render_template('admin/vip_buy.html', car=car)
        else:
            car = BuyCar.query.filter_by(users=user_id).all()
            return render_template('admin/vip_buy.html', car=car)


# 收藏
@admin.route('/vip/col=<string:user_id>')
@admin.route('/vip/col=/')
@login_required
def vip_col(user_id=None):
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        if user_id == None:
            col = Collect.query.all()
            return render_template('admin/vip_col.html', col=col)
        else:
            col = Collect.query.filter_by(users=user_id).all()
            return render_template('admin/vip_col.html', col=col)


# 评论
@admin.route('/vip/com=<string:user_id>')
@admin.route('/vip/com=/')
@login_required
def vip_com(user_id=None):
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        if user_id == None:
            com = Comment.query.all()
            return render_template('admin/vip_com.html', com=com)
        else:
            com = Comment.query.filter_by(users=user_id).all()
            return render_template('admin/vip_com.html', com=com)


# 查看所有操作日志
@admin.route('/logs')
@admin.route('/logs/id=<int:user_id>')
@login_required
def logs(user_id=None):
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        if user_id == None:
            log = UserLog.query.all()
            return render_template('admin/logs.html', log=log)
        else:
            log = UserLog.query.filter_by(users=user_id).all()
            return render_template('admin/logs.html', log=log)


# 查看统计数据
@admin.route('/count')
@login_required
def count():
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        info = Count.query.first()
        return render_template('admin/count.html', info=info)

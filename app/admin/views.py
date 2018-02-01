from . import admin
from app import db
from flask import render_template, flash, redirect, request, session, url_for
from flask_login import login_required, current_user
from app.model import Count, Goods, Tag, Tags, TagList
from .form import AddGoodsForm
import time


# 后台管理主页
@admin.route('/')
@login_required
def index():
    username = current_user.username
    if username == "admin":
        info = Count.query.first()
        return render_template('admin/index.html', count=info)
    else:
        tag_list = TagList.query.all()
        tags = Tags.query.all()
        tag = Tag.query.all()
        shops = Goods.query.all()
        return render_template('home/index.html', tag_list=tag_list,
                               shops=shops, tags=tags, tag=tag)


# 商品添加页面
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
        inf = Goods(
            good_id=int(time.time()),
            name=form.name.data,
            good_tag=form.good_tag.data,
            chap_num=form.chap_num.data,
            price=form.price.data,
            old_price=form.old_price.data,
            start=form.start.data,
            discount=(float(form.price.data)
                      / float(form.old_price.data)),
            course_info=form.info.data,
            target=form.target.data,
        )
        # db.session.add(inf)
        # db.session.commit()
        flash("添加成功", 'ok')
        return redirect('admin.add_good')
    return render_template('admin/add_goods.html', form=form)


# 富文本内容编辑 也就是商品详情编辑
@admin.route('/upload/', methods=['GET', 'POST'])
def upload():
    print(request.method)
    if request.method == "POST":
        print(request.get_data())
    pass


# 等待上架商品
@admin.route('/wait_goods/')
@login_required
def wait_goods():
    username = current_user.username
    if username != "admin":
        flash("请使用admin账号登陆")
        return redirect(url_for('auth.login'))
    else:
        return render_template('admin/wait_goods.html')


# 出售中商品
@admin.route('/wait_goods/')
@login_required
def sale_goods():
    username = current_user.username
    if username != "admin":
        flash("请使用admin账号登陆")
        return redirect(url_for('auth.login'))
    else:
        return render_template('admin/sale_goods.html')


# 查看所有商品信息
@admin.route('/goods')
@login_required
def goods_list():
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        return render_template('admin/goods.html')


# 商品编辑页面
@admin.route('/edit_goods')
@admin.route('/edit_goods/<int:goods_id>')
@login_required
def edit_good(goods_id):
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        return render_template('admin/edit_goods.html')


# 查看所有订单页面
# 修改订单页面
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
        return render_template('admin/orders.html')


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
        return render_template('admin/comments.html')


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
        return render_template('admin/vip.html')


# 会员订单
@admin.route('/vip/order=<int:order_id>')
@admin.route('/vip/')
@login_required
def vip_order(order_id=None):
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        return render_template('admin/vip_order.html')


# 购物车
@admin.route('/vip/buy=<string:user_id>')
@admin.route('/vip/')
@login_required
def vip_buy(user_id=None):
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        return render_template('admin/vip_buy.html')


# 收藏
@admin.route('/vip/col=<string:user_id>')
@admin.route('/vip/')
@login_required
def vip_col(user_id=None):
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        return render_template('admin/vip_col.html')


# 评论
@admin.route('/vip/com=<string:user_id>')
@admin.route('/vip/')
@login_required
def vip_com(user_id=None):
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        return render_template('admin/vip_com.html')


# 查看所有操作日志
@admin.route('/logs')
@login_required
def logs():
    username = current_user.username
    if username != "admin":
        flash("该用户为普通用户")
        flash("请使用admin管理员账号登陆！")
        return redirect(url_for('auth.login'))
    else:
        return render_template('admin/logs.html')


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
        return render_template('admin/count.html')

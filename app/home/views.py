from flask import render_template
from . import home
from app.model import TagList, Tags, Tag, Goods
from app import db


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
    return render_template('home/index.html', tag_list=tag_list, tags=tags, tag=tag)


# 分类列表页 二级
@home.route('/tag=<int:tag>')
def tag(tag):
    name = TagList.query.filter_by(id=tag).first()
    tags = Tags.query.filter_by(f_name=name.name).all()
    return render_template('home/tag.html', tags=tags, Tag=Tag, Goods=Goods)


# 分类列表页 三级
@home.route('/tag=<int:tag>/tags=<int:tags>')
def theree_tag(tag, tags):
    return "{}===={}".format(tag, tags)


# 详情页
@home.route('/detail/goods=<string:goods_id>')
def detail(goods_id):
    return ""


# 购物车页
@home.route('/buy')
def buy():
    return ""


# 结算页
@home.route('/pay')
def pay():
    return ""


# 搜索页
@home.route('/search')
def search():
    return ""


# 登录页
@home.route('/login')
def login():
    return ""


# 注册页
@home.route('/register')
def register():
    return ""


@home.route('/logout')
def logout():
    return ""


# 个人中心
@home.route('/user')
def user():
    return ""


# 订单详情页
@home.route('/order')
def order():
    return ""


# 我的订单
@home.route('/order_list')
def order_list():
    return ""


# 收藏商品列表
@home.route('/collect')
def collect():
    return ""


# 联系我们
@home.route('/connect')
def connect():
    return ""


# 帮助中心
@home.route('/help')
def help():
    return ""


# 关于我们
@home.route('/about')
def about():
    return ""


# 购物流程介绍
@home.route('/buytip')
def how_to_buy():
    return ""


# 常见问题
@home.route('/question')
def question():
    return ""


# 取消订单
@home.route('/cancel')
def cancel_order():
    return ""


# 售后服务
@home.route('/service')
def service():
    return ""


# 网站导航
@home.route('/map')
def map():
    return ""


# 修改密码页面
@home.route('/pwd')
def change_pwd():
    return ""

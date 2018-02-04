from django.shortcuts import render
# 自定义模型类
from .models import *
# 包装类
from utils.wrappers import *
# 函数类
from .functions import *
# 分页器
from django.core.paginator import Paginator


# 商品首页
@get_total
def index(request):
    # 获取广告分类
    ads = Advertisement.objects.all()
    adv1 = ads[:4]
    adv2 = ads[4:]
    # 获取商品分类
    cags = Category.objects.all()
    for cag in cags:
        # 获取最热的三个商品
        hot = GoodsInfo.objects.get_hot_by_cag(cag)
        # 获取最新的的四个商品
        new = GoodsInfo.objects.get_new_by_cag(cag)
        cag.hot = hot
        cag.new = new
    return render(request, 'goods/index.html', locals())


# 商品列表
@get_total
def goods_list(request, cag_id, page_id):
    # 查找商品种类
    cags = Category.objects.all()
    # 查找所有商品中最热的两个
    goods_hot = GoodsInfo.objects.get_hot_by_all()
    # 获取当前的显示方式query
    show = get(request, 'show')
    # 获取指定产品分类的所有商品
    goods_spec = GoodsInfo.objects.get_goods_by_cag(cag_id, show)
    # 设置分页器
    paginator = Paginator(goods_spec, 10)
    paginator_goods = paginator.page(page_id)
    return render(request, 'goods/list.html', locals())


# 商品详情
@get_total
def detail(request):
    # 查找商品种类
    cags = Category.objects.all()
    # 获取查询的商品
    goods = GoodsInfo.objects.get(pk=int(get(request, 'id')))
    # 获取所有商品中最热的两个
    goods_hot_all = GoodsInfo.objects.get_hot_by_all()
    # 记录商品的浏览信息
    record_goods_browser(request)
    return render(request, 'goods/detail.html', locals())

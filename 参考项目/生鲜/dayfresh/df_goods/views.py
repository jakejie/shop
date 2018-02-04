# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import *
from df_cart.models import *
from django.core.paginator import Paginator


def list(req, tid, pindex, sort):
    typeinfo = TypeInfo.objects.get(id=int(tid))
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort == '1':  #默认，最新
        goods_list = GoodsInfo.objects.filter(gtype=int(tid)).order_by('-id')
    elif sort == '2':  # 价格
        goods_list = GoodsInfo.objects.filter(gtype=int(tid)).order_by('-gprice')
    elif sort == '3':  # 人气，点击量
        goods_list = GoodsInfo.objects.filter(gtype=int(tid)).order_by('-gclick')
    paginator = Paginator(goods_list, 10)
    page = paginator.page(int(pindex))
    context = {
        'title': '天天生鲜-商品列表',
        'ttitle': typeinfo.ttitle,
        'page': page,
        'paginator': paginator,
        'typeinfo': typeinfo,
        'sort': sort,
        'news': news,
        'cart_count': cart_count(req),
    }
    return render(req, 'df_goods/list.html', context)

def detail(req, gid):
    goods = GoodsInfo.objects.get(id=int(gid))
    goods.gclick += 1
    goods.save()
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {
        'title': '天天生鲜-商品详情',
        'ttitle': goods.gtype.ttitle,
        'goods': goods,
        'news': news,
        'id': gid,
        'cart_count': cart_count(req),
    }
    res = render(req, 'df_goods/detail.html', context)
    #通过id记录最近浏览内容
    goods_ids = req.COOKIES.get('goods_ids', '')
    if goods_ids != '':  #判断是否有浏览记录
        goods_id_list = goods_ids.split(',')
        if goods_id_list.count(gid) >=1:  #如果商品已有记录则删除当次浏览
            goods_id_list.remove(gid)
        goods_id_list.insert(0, gid)
        if len(goods_id_list) >=6:  #超过6个则删除最后一个
            del goods_id_list[5]
        goods_ids = ','.join(goods_id_list)
    else:
        goods_ids = gid  #之前没浏览记录则直接添加
    res.set_cookie('goods_ids', goods_ids)

    return res

def index(req):
    #查询各种类下最新4条数据，点击量最多的3条数据
    typelist = TypeInfo.objects.all()
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:3]
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:3]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:3]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:3]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:3]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:3]
    context = {'title': '首页',
               'type0': type0, 'type01': type01,
               'type1': type1, 'type11': type11,
               'type2': type2, 'type21': type21,
               'type3': type3, 'type31': type31,
               'type4': type4, 'type41': type41,
               'type5': type5, 'type51': type51,
               'cart_count': cart_count(req),
               }
    return render(req, 'df_goods/index.html', context)

# 购物车数量(封装的一个方法查询购物车中商品数量)
def cart_count(request):
  if request.session.has_key('user_id'):
    return CartInfo.objects.filter(user_id=request.session['user_id']).count()
  else:
    return 0
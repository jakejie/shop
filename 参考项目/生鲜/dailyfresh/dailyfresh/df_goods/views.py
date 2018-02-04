from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator, Page


# from django.conf.urls import


def home_list_page(request):
    typelist = TypeInfo.objects.all()
    # orderby(-id)表示降序,否则是升序
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]

    # typelist = TypeInfo.objects.all()
    # type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    # print(type0)
    # type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]

    # context = {'title': '天天生鲜首页','haslogin': haslogin}
    context = {'title': '天天生鲜首页', 'type0': type0, 'type1': type1, 'type2': type2,
               'type3': type3, 'type4': type4, 'type5': type5}
    return render(request, 'df_goods/index.html', context)


def typeInfo(request):
    # 这里添加分页信息

    id = request.GET['typeid']
    pindex = request.GET['pindex']
    pindex = int(pindex)
    list = GoodsInfo.objects.filter(gtype_id=id)
    # 将查询结果集分页 输入结果集和每页条数
    paginator = Paginator(list, 10)
    # 返回第几页
    page = paginator.page(pindex)
    # print(list[0].gpic)
    context = {'title': '天天生鲜-商品列表', 'paginator': paginator, 'list': page, 'typeid': id}
    # print(str(page.has_previous()))
    return render(request, 'df_goods/list.html', context)


def detail(request):
    goodid = request.GET['goodid']
    # print(goodid)
    good = GoodsInfo.objects.get(id=goodid)
    good.gclick = good.gclick + 1
    a = request.COOKIES.get('aaa', '')
    print(type(a))
    good.save()
    context = {'title': '天天生鲜-商品详情', 'good': good}
    response = render(request, 'df_goods/detail.html', context)

    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id = '%d' % good.id
    if goods_ids != '':  # 判断是否有浏览记录，如果有则继续判断
        goods_ids1 = goods_ids.split(',')  # 拆分为列表
        if goods_ids1.count(goods_id) >= 1:  # 如果商品已经被记录，则删除
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0, goods_id)  # 添加到第一个
        if len(goods_ids1) >= 6:  # 如果超过6个则删除最后一个
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)  # 拼接为字符串
    else:
        goods_ids = goods_id  # 如果没有浏览记录则直接加
    response.set_cookie('goods_ids', goods_ids)  # 写入cookie

    return response

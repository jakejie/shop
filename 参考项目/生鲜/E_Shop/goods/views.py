#! /usr/bin env python3
# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from view.views import BaseView
from utils.pageutils import MultiObjectReturned
from goods.models import *


# 对商品信息进行渲染
class GoodsListView(BaseView, MultiObjectReturned):
    template_name = 'index.html'
    objects_name = 'goods'
    category_objects = Category.objects.all()

    def prepare(self, request):
        # 获取当前页面的类型id,如果没有获取到就使用默认值
        category_id = int(request.GET.get('category', Category.objects.first().id))
        self.objects = Category.objects.get(id=category_id).goods_set.all()
        self.category_id = category_id

    def get_extra_context(self, request):
        page_num = request.GET.get('page', 1)
        context = {
            'category_id': self.category_id,
            'categorys': self.category_objects
        }
        context.update(self.get_objects(page_num))
        return context


# 处理商品详情页面
class GoodsDetailsView(BaseView):
    template_name = 'details.html'

    # 数据预处理
    def prepare(self, request, num, *args, **kwargs):
        # 获取当前页面的类别，商品信息
        goods_id = int(num)
        self.goods = Goods.objects.get(id=goods_id)
        self.category = self.goods.categoryid
        self.goods_details = Goodsdetails.objects.filter(goodsid=goods_id)

        for item in self.goods.size().keys():
            goods_size = item
            break

        self.size = request.GET.get('size', goods_size)
        self.color = request.GET.get('color', self.goods.color().first().color.id)

    # 读取cookie
    def handle_request_cookie(self, request, *args, **kwargs):
        goods_history_id = request.COOKIES.get('goods_history')

        if goods_history_id is None:
            goods_history_id = []
        else:
            goods_history_id = eval(goods_history_id)

        self.goods_history = []

        # 根据cookie中的id获取goods对象
        for goods_history_id_item in goods_history_id:
            self.goods_history.append(Goods.objects.get(id=goods_history_id_item))

    # 存入cookie
    def handle_response_cookie(self, response, *args, **kwargs):
        goods_history = self.request.COOKIES.get('goods_history')
        if goods_history is None:
            goods_history = [self.goods.id]
        else:
            goods_history = eval(goods_history)
            if len(goods_history) > 5:
                goods_history.pop(0)
            else:
                if self.goods.id not in goods_history:
                    goods_history.append(self.goods.id)

        response.set_cookie('goods_history', str(goods_history), path='/details')

    # 设置渲染内容
    def get_extra_context(self, request):
        context = {
            'category': self.category,
            'goods': self.goods,
            'goods_details': self.goods_details,
            'goods_size_current': self.size,
            'goods_color': self.color,
            'goods_history': self.goods_history
        }

        return context

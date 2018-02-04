#-*-coding:utf-8-*-
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^place_order/$', place_order, name='place_order'),  # 订单
    url(r'^order_handle/$', order_handle, name='order_handle'),  # 订单处理
]

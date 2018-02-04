#! /usr/bin env python3
# -*- coding:utf-8 -*-

from django.conf.urls import url

from order import views

urlpatterns=[
    url(r'^$', views.OrderView.as_view()),
    url(r'^orderlist/$', views.OrderListView.as_view()),
    url(r'^created/$', views.OrderCreatedView.as_view()),
    url(r'^alipay/$', views.AliPayView.as_view()),
]
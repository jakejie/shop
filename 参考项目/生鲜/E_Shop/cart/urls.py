#! /usr/bin env python3
# -*- coding:utf-8 -*-

from django.conf.urls import url
from cart import views

urlpatterns = [
    url(r'^$', views.CartView.as_view()),
    url(r'^cart.html/$', views.GoodsCartView.as_view()),

]
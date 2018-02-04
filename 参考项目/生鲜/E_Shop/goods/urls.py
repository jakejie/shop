#! /usr/bin env python3
# -*- coding:utf-8 -*-
from django.conf.urls import url
from goods import views

urlpatterns = [
    url(r'^$', views.GoodsListView.as_view()),
    url(r'details/(\d+)', views.GoodsDetailsView.as_view()),
]

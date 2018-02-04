# -*- coding: utf-8 -*-
from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.order, name='suborder'),
    url(r'^order_handle/', views.order_handle, name='order_handle'),
    url(r'^pay(\d+)/', views.pay, name='pay'),
]
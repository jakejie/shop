# -*- coding: utf-8 -*-
from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.cart, name='subcart'),
    url(r'^add(\d+)_(\d+)/', views.add, name='add'),
    url(r'^edit(\d+)_(\d+)/', views.edit, name='edit'),
    url(r'^delete(\d+)/', views.delete, name='delete'),
]
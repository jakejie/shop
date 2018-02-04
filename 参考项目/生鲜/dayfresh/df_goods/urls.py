# -*- coding: utf-8 -*-
from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(\d+)/', views.detail, name='detail'),
    url(r'^list(\d+)_(\d+)_(\d+)', views.list, name='list'),
]
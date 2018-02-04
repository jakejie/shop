#-*-coding:utf-8-*-
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', user_center_info, name='user_center_info'),  # 用户中心信息
    url(r'^register/$', register, name='register'),  # 用户注册
    url(r'^register_handle/$', register_handle, name='register_handle'),  # 用户注册处理
    url(r'^register_check_username/$', register_check_username, name='register_check_username'),  # 用户注册检查用户名
    url(r'^login/$', login, name='login'),  # 用户登录
    url(r'^login_handle/$', login_handle, name='login_handle'),  # 检查登录参数
    url(r'^logout/$', logout, name='logout'),  # 注销登录
    url(r'^user_center_site/$', user_center_site, name='user_center_site'),  # 用户中心地址
    url(r'^user_center_site_edit/$', user_center_site_edit, name='user_center_site_edit'),  # 编辑地址
    url(r'^user_center_order/$', user_center_order, name='user_center_order'),  # 用户中心订单
]

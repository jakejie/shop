"""ttsx_all URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.views.static import serve
from django.conf import settings
from users.views import user_center_info

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),  # 后台管理
    url(r'^$', user_center_info, name='index'),
    url(r'^users/', include('users.urls', namespace='users')),  # 用户
    url(r'^goods/', include('goods.urls', namespace='goods')),  # 商品
    url(r'^carts/', include('carts.urls', namespace='carts')),  # 购物车
    url(r'^order/', include('order.urls', namespace='order')),  # 订单
    url(r'^search/', include('haystack.urls')),  # 配置全文搜索引擎
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),  # 配置全文搜索引擎
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico', permanent=False)),  # 获取网站图标
]

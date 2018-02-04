# coding=utf-8

from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^user_info/$',userInfo,name = 'user_info'),
    url(r'^user_order/(?P<pageIndex>[1-9]+\d*)/$',userOrder,name = 'userOrder'),
    url(r'^user_site/$',userSite,name = 'userSite'),
    url(r'^addressAddHandler/$',addressAddHandler,name = 'addressAddHandler'),
    url(r'^addGoodsHanderler/$',addGoodsHanderler,name= 'addGoodsHanderler'),

]

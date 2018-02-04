from django.conf.urls import url
from views import *

urlpatterns = [
	url(r'^$',index,name='index'),
	url(r'^goodsType/$',goodsType,name='goodsType'),
	url(r'^detail/$',detail,name='detail'), 
    url(r'^exit/$',exit,name='exit'),
    url(r'^saveGoodsID/$',saveGoodsID,name='saveGoodsID'),
]
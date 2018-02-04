from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^cart/$',myCart,name='cart'),
    url(r'^placeOrder/$',placeOrder,name='placeOrder'), 
    url(r'^delGoodsHandeler/$',delGoodsHandeler,name='delGoodsHandeler'), 
    url(r'^filterDataHandeler/$',filterDataHandeler,name='filterDataHandeler'),
    ] 
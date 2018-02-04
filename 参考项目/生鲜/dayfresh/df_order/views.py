# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from models import *
from df_user import login_check
from df_user.models import *
from df_cart.models import *
from django.db import transaction
from datetime import datetime
from decimal import Decimal


@login_check.login
def order(req):
    user = UserAddress.objects.get(user=req.session['user_id'])
    get = req.GET
    cart_ids = get.getlist('cart_id')
    cart_idlist = [int(item) for item in cart_ids]
    carts = CartInfo.objects.filter(id__in=cart_idlist)
    context = {
        'title': '提交订单',
        'subtitle': '提交订单',
        'carts': carts,
        'user': user,
        'cart_ids': ','.join(cart_ids),
    }
    return render(req, 'df_order/place_order.html', context)

def order_handle(req):
    tran_id = transaction.savepoint()
    cart_ids = req.POST.get('cart_ids')
    order = OrderInfo()
    try:
        now = datetime.now()
        uid = req.session['user_id']
        order.oid = '%s%s'%(now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = int(uid)
        order.odate = now
        order.ototal = Decimal(req.POST.get('total'))
        order.oaddress = req.POST.get('address')
        order.save()
        cart_idlist = [int(item) for item in cart_ids.split(',')]
        for id in cart_idlist:
            detail = OrderDetailInfo()
            detail.order = order
            cart = CartInfo.objects.get(id=id)
            #判断商品库存
            goods = cart.goods
            if goods.ginventory >= cart.count: #如果库存大于购买数量
                goods.ginventory -= cart.count #减少商品库存
                goods.save()
                # 完善详单信息
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()
                # 删除购物车数据
                cart.delete()
            else: #如果库存小于购买数量
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print '=================%s'%e
        transaction.savepoint_rollback(tran_id)
    return redirect('/order/pay%s'%order.oid)

def pay(req, oid):
    order = OrderInfo.objects.get(oid=oid)
    order.oIsPay = True
    order.save()
    context = {'order': order}
    return render(req, 'df_order/pay.html', context)
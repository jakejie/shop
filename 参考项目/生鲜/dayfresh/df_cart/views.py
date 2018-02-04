# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import JsonResponse
from df_user import login_check
from models import *

@login_check.login
def cart(req):
    # 登录状态已写入session信息，直接读取
    uid = req.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    context = {
        'title': '天天生鲜-购物车',
        'subtitle': '购物车',
        'carts': carts,
    }
    return render(req, 'df_cart/cart.html', context)

@login_check.login
def add(req, gid, count):
    uid = req.session['user_id']
    gid = int(gid)
    count = int(count)
    #查询购物车是否有此商品，有则数量增加，没有则加入
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count += count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()
    mount = CartInfo.objects.all().count()
    return JsonResponse({'count': mount, 'cart_id': cart.id})

def edit(req, cid, count):
    count1 = 1
    try:#get查询不到会报异常
        cart = CartInfo.objects.get(id=int(cid))
        count1 = cart.count
        cart.count = int(count)
        cart.save()
        data = {'ok': 0}
    except Exception as e:
        data = {'ok': count1}
    return JsonResponse(data)

def delete(req, cid):
    try:
        cart = CartInfo.objects.get(id=int(cid))
        cart.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': 0}
    return JsonResponse(data)
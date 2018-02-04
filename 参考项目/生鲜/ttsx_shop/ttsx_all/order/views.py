from django.shortcuts import render
import time
import random
from django.db import transaction
from django.http import JsonResponse
from carts.models import *
from users.models import *
from .models import *
from utils.wrappers import *


# 订单
def place_order(request):
    # 获取所有商品id
    goods_id = post_list(request, 'goods_id')
    # print(goods_id)
    # 拼接商品id
    goods_list = ':'.join(goods_id)
    # 获取所有商品
    carts = Carts.objects.filter(cart_user_id=get_session(request, 'uid'), cart_goods_id__in=goods_id)
    # print(carts)
    # 记录商品总价
    carts.total = 0
    # 记录商品总量
    carts.amount = 0
    for cart in carts:
        # 记录商品单品总价
        cart.single = cart.cart_goods.goods_price * cart.cart_amount
        # print(cart.single)
        carts.total += cart.single
        carts.amount += cart.cart_amount
    # 查找个人信息
    user = User.objects.user_by_username(get_session(request, 'user_name'))
    return render(request, 'order/place_order.html', locals())


# 订单处理
@transaction.atomic
def order_handle(request):
    # 获得订单商品ID
    goods_id = post(request, 'id').split(':')
    # 获得支付方式
    pay_style = post(request, 'pay')
    # 获得用户ID
    user_id = get_session(request, 'uid')
    # 获取购物车商品信息
    carts = Carts.objects.filter(cart_user_id=user_id, cart_goods_id__in=goods_id)
    # 查询用户
    user = User.objects.get(id=user_id)
    # 创建保存点
    save_point = transaction.savepoint()
    try:
        # 创建订单信息
        order = Order()
        order.order_user = user
        order.order_pay = pay_style
        order.order_addr = user.user_addr
        order.order_recv = user.user_recv
        order.order_tele = user.user_phone
        # 订单编号(用户ID + 时间戳 + 随机值)
        order.order_number = str(user_id) + str(int(time.time())) + str(random.randint(1000, 9999))
        order.save()
        for cart in carts:
            # 创建商品订单信息
            gd = GoodsDetail()
            gd.goods_name = cart.cart_goods.goods_name
            gd.goods_price = cart.cart_goods.goods_price
            gd.goods_unit = cart.cart_goods.goods_unit
            gd.goods_num = cart.cart_amount
            gd.goods_img = cart.cart_goods.goods_image
            gd.goods_order = order
            gd.save()
        # 删除购物车中相应商品的信息
        carts.delete()
        # 提交操作
        transaction.savepoint_commit(save_point)
    except Exception as e:
        # 如果操作出错，滚回去
        transaction.savepoint_rollback(save_point)
        return JsonResponse({'ret': 0})
    return JsonResponse({'ret': 1})

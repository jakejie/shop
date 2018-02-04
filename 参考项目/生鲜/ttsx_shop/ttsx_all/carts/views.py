from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from .models import *
from utils.wrappers import *


# 购物车
def cart(request):
    # 查找购物车中所有商品记录
    try:
        carts = Carts.objects.filter(cart_user_id=get_session(request, 'uid'))
        # print(carts)
    except ValueError:
        return redirect(reverse('users:login'))
    # 记录商品总价
    carts.total = 0
    # 记录商品总数量
    carts.amount = 0
    for cart in carts:
        cart.single = cart.cart_goods.goods_price * cart.cart_amount
        carts.total += cart.single
        carts.amount += cart.cart_amount
    return render(request, 'carts/cart.html', locals())


# 商品加入购物车
def add_carts(request):
    user_id = get_session(request, 'uid')
    user_name = get_session(request, 'user_name')
    # 1.判断用户是否登录
    if not (user_id and user_name):
        return JsonResponse({'total': 0})
    # 2.获取商品信息
    goods_id = get(request, 'goods_id')
    goods_num = get(request, 'goods_num')
    # 3.信息入库
    try:
        # 3.1 如果商品已经存在，则更新商品数量和修改时间
        record = Carts.objects.get(cart_goods_id=goods_id, cart_user_id=user_id)
        record.cart_amount = record.cart_amount + int(goods_num)
        record.save()
    except Carts.DoesNotExist:
        # 3.2 如果商品不存在，则更新用户信息、商品数量和商品信息
        record = Carts()
        record.cart_goods_id = goods_id
        record.cart_user_id = user_id
        record.cart_amount = goods_num
        record.save()
    # 4.返回购物车总数
    total = Carts.objects.filter(cart_user_id=user_id).aggregate(models.Sum("cart_amount"))
    return JsonResponse({'total': total['cart_amount__sum']})


# 编辑商品购物车
def edit_carts(request):
    # 获取商品id
    goods_id = get(request, 'id')
    # 获取商品数量
    goods_num = get(request, 'num')
    # 信息入库
    try:
        # 记录存在, 更新商品数量
        cart = Carts.objects.get(cart_user_id=get_session(request, 'uid'), cart_goods_id=goods_id)
        cart.cart_amount = goods_num
        cart.save()
    except Carts.DoesNotExist:
        # 返回接收失败
        return JsonResponse({'ret': 0})
    return JsonResponse({'ret': 1})


#  删除商品购物车
def delete_carts(request):
    # 获取商品id
    goods_id = get(request, 'id')
    # 信息入库
    try:
        # 记录存在, 删除商品
        cart = Carts.objects.get(cart_user_id=get_session(request, 'uid'), cart_goods_id=goods_id)
        cart.delete()
    except Carts.DoesNotExist:
        # 返回接收失败
        return JsonResponse({'ret': 0})
    return JsonResponse({'ret': 1})

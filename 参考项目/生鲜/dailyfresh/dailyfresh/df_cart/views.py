from django.shortcuts import render
from .models import CartInfo
from django.http.response import JsonResponse,HttpResponseRedirect
from django.db.models import Q
from . import cart_decorator


def base_query(request):
    user_id = request.session['user_id']
    list = CartInfo.objects.filter(user_id=user_id)
    goods = []
    totalPrice = 0
    for item in list:
        # 遇到下面这中情形,除了goods信息外,还需要往前端传递一个计数的信息,便可以利用python动态语言的性质
        # 直接item.counta 为item添加一个新的属性,然后前端获取item.counta即可
        item.counta = int(item.count)
        item.price = float(item.goods.gprice)
        item.subprice = item.counta*item.price
        goods.append(item)
        totalPrice += item.count * item.goods.gprice
    return render(request, 'df_cart/cart.html', {'goods': goods, 'totalPrice': totalPrice})


@cart_decorator.login
def index(request):
    return base_query(request)


# 这一步还是用ajax做比较方便
@cart_decorator.login
def addcart(request, goodid, count):
    # print(goodid)
    cart = CartInfo()
    cart.count = count
    cart.goods_id = goodid
    user_id = request.session['user_id']
    cart.user_id = user_id
    count = len(CartInfo.objects.filter(user_id=user_id))
    cart.save()
    return JsonResponse({'count': count})


@cart_decorator.login
def tocart(request, goodid, count):
    user_id = request.session['user_id']
    good = CartInfo.objects.filter(Q(user_id=user_id), Q(goods_id=goodid))
    if len(good)==0:
        cart = CartInfo()
        cart.count = count
        cart.goods_id = goodid
        cart.user_id = user_id
        cart.save()
    else:
        good[0].count += int(count)
        good[0].save()

    return base_query(request)

@cart_decorator.login
def delete(request, goodid):
    user_id = request.session['user_id']
    CartInfo.objects.filter(Q(user_id=user_id), Q(goods_id=goodid)).delete()

    return base_query(request)
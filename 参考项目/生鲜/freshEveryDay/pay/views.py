# coding=utf-8

from django.core.urlresolvers import reverse 
from django.shortcuts import render,redirect
from login import decrotors
from pay.models import *
from goods_info.models import *
from login.models import user_info
from django.http import HttpResponse,JsonResponse
import json

@decrotors.login
def myCart(request,dic):
	goodsList = []
	# 商品合计总价
	allGoodsPrice = 0
	userID = user_info.objects.get(name=dic['userName']).pk
	cartGoods = cart.objects.filter(user_id_id=userID)
	goodsCount = cart.objects.filter(user_id_id=userID).count()
	for good in cartGoods:
		goodID = good.goods_id_id
		goodInfo = goods_info.objects.get(pk=goodID)
		goodsList.append(goodInfo)	
	goodsList = list(set(goodsList))
	for goods in goodsList:
		sumPrice = goods.getSumPrice()
		allGoodsPrice+=sumPrice
	dic['goodsList'] = goodsList
	dic['goodsCount'] = goodsCount
	dic['allGoodsPrice'] = allGoodsPrice
	return render(request,'pay/cart.html',dic)

def delGoodsHandeler(request):
	if request.method =='POST':
		goodsID = int(request.POST['goodsID'])
		print goodsID
		cart2 = cart.objects.get(goods_id_id=goodsID)
		cart2.delete()
		flag=json.dumps({'isDelete':1})
		return jsonResponse(json.dumps(flag))


@decrotors.login
def placeOrder(request,dic):
	return render(request,'pay/place_order.html',dic)   


def filterDataHandeler(request):
	dataNum = len(request.POST)/3
	for i in range(dataNum):
		ID = request.POST['goods['+ str(i) +'][id]']
		isChecked = request.POST['goods['+ str(i) +'][isChecked]']
		# 数据被选中，更新数量
		if int(isChecked) == 1:
			cartInfo = cart.objects.get(goods_id_id=int(ID))
			count = request.POST['goods['+ str(i) +'][count]']
			dataInfo = cart.objects.get(goods_id_id=int(ID))
			dataInfo.buy_count = count
			dataInfo.save()
		else:
			cartInfo = cart.objects.get(goods_id_id=int(ID))
			cartInfo.delete()
	
	return HttpResponse('123')

	

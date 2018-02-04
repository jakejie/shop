#coding=utf-8

from django.core.urlresolvers import reverse   
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from login.models import user_info
from goods_info.models import *
from models import *
from pay.models import cart
from toolKit import *
from login import decrotors

# 用户中心-个人信息视图函数
@decrotors.login
def userInfo(request,dic):
	goodsList = []
	goods_detail = []
	userName = dic['userName']
	userInfo = user_info.objects.get(name=userName)
	id = userInfo.pk
	name = userInfo.name
	telephone = userInfo.phone_number
	address = userInfo.address
	json_info = {'name':name,'phone_number':telephone,'address':address}
	recent_list = recent_views.objects.order_by('-view_time').all().filter(user_id = id)[:5]
	for goods in recent_list:
		goods_id = goods.goods_id_id		
		goodsList.append(goods_id)
	for i in goodsList:
		goods = goods_info.objects.get(id=i)
		name = goods.name
		img_url = goods.img_url
		price = goods.price
		unit = goods.unit
		goods_detail.append({'name':name,'img_url':img_url,'price':price,'unit':unit})
	return render(request,'person_info/user_center_info.html',{'user_info':json_info,'goods_detail':goods_detail,'userName':userName})

# 用户中心-个人信息视图函数
# 需要查询的数据：
# 下单时间、订单号、支付状态、商品名称、商品价格、单位、图片url、购买数量
def userOrder(request,pageIndex):
	userName = request.session.get('userName',default='')
	dic={
		'userName':userName
	}
	userInfo = user_info.objects.get(name=userName)
	userID = userInfo.pk
	orderList = orders.objects.filter(user_id_id=userID).order_by('-order_time')
	allInfo = []
	tempList = []
	# 某用户的订单号的集合
	orderIDList = []
	orderPriceList=[]
	for i in orderList:
		orderIDList.append(i.pk)

	for orderID in orderIDList:
		goodsInfoList = []
		order = orders.objects.get(pk=orderID)
		isPay = order.is_pay
		orderTime = formateTime(order.order_time)
		sumPrice = 0
		# 获取一个订单中的所有商品id
		goodsID = order_record.objects.filter(order_id_id=orderID)
		for num in goodsID:
			goodsInfo = goods_info.objects.get(pk=num.goods_id_id)
			goodsName = goodsInfo.name
			goodsPrice = goodsInfo.price
			goodsUnit = goodsInfo.unit
			goodsUrl = str(goodsInfo.img_url)
			goodsCount = order_record.objects.filter(order_id_id=orderID).filter(goods_id_id=num.goods_id_id)
			goodsPriceSum = goodsPrice * goodsCount[0].goods_count
			sumPrice += goodsPriceSum			
			goodsItem = {'orderID':orderID,'goodsName':goodsName,'goodsPrice':goodsPrice,'goodsUnit':goodsUnit,'goodsUrl':goodsUrl,'goodsCount':goodsCount[0].goods_count,'goodsPriceSum':goodsPriceSum}
			goodsInfoList.append(goodsItem)
			orderPrice = (orderID,sumPrice)
		info = {'orderID':orderID,'orderTime':orderTime,'isPay':isPay,'orderGoodsInfo':goodsInfoList,'sumPrice':sumPrice}
		allInfo.append(info)
		tempList = allInfo
		# 更新数据库中的订单总价
		orderPriceList.append((orderPrice))
		for i in orderPriceList:
			orderID = i[0]
			price = i[1]
			table = orders.objects.get(pk=orderID)
			if table.total_price == 0:
				table.total_price = price
				table.save()
	# 分页
	p = Paginator(tempList,3)
	pIndex = int(pageIndex)
	if pIndex == 0:
		pIndex = 1
	list2 = p.page(pIndex)
	prange = p.page_range		
	return render(request,'person_info/user_center_order.html',{'allInfo':list2,'prange':prange,'pIndex':pIndex,'dic':dic})


# 用户中心-收货地址视图函数
@decrotors.login
def userSite(request,dic):	
	reli_name = request.session.get('name')
	address = request.session.get('address')
	number = request.session.get('phone_number')
	if reli_name and address and address:
		json_info = {'address':address,'name':reli_name,'phone_number':number}
	else:
		address_list = deli_address.objects.filter(user_id_id=1).all().order_by('-id')
		address = address_list[0].detail_address
		reli_name = address_list[0].deli_name
		number = formatPhoneNumber(address_list[0].phone_number)
		json_info = {'address':address,'name':reli_name,'phone_number':number}
	return render(request,'person_info/user_center_site.html',{'json_info':json_info,'dic':dic})

# 增加收货地址
# 如果能在session中能查到数据，那么从session中获取数据，否则查数据库中的最后一条
def addressAddHandler(request):
	if request.method == 'POST':
		name = request.POST['name']
		address = request.POST['address']
		postcode = request.POST['postcode']
		phone_number = request.POST['phone_number']
		new_phone_num = formatPhoneNumber(phone_number)
		info = [name,address,postcode,new_phone_num]
	address_info = deli_address(user_id_id=1,deli_name=name,detail_address=address,postcode=postcode,phone_number=phone_number)
	address_info.save()
	request.session['name']=name
	request.session['address']=address
	request.session['phone_number']=phone_number
	request.session.set_expiry(0)
	return redirect(reverse('freshEveryDay:userSite'))

# 购物车增加商品
@decrotors.login
def addGoodsHanderler(request,dic):
	if request.method == 'POST':
		# 传过来的name是购物车中的商品名称
		name = request.POST['name']
		# 获取当前用户ID
		userName = dic['userName']
		user_id = user_info.objects.get(name=userName).pk
		# 获取名称为name的商品信息
		goodsInfo = goods_info.objects.get(name=name)			
		goodsID = goodsInfo.pk
		# 获取购物车中是否有id为goodsID的商品
		cartGoods = cart.objects.filter(goods_id_id=goodsID)
		if len(cartGoods)>0:
			cartGoods[0].buy_count += 1
			cartGoods[0].save()
		else:
			cart_goods = cart(buy_count=1,goods_id_id=goodsID,user_id_id=user_id)
			cart_goods.save()




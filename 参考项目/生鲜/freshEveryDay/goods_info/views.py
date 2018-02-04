#coding=utf-8
from django.core.urlresolvers import reverse   
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from login import decrotors
from goods_info.models import *
from person_info.models import *
from login.models import *
import json


# 需要查询的数据  
# 1.商品分类 2.商品名称、价格、图片url
@decrotors.login
def index(request,dic):
    cates = goods_cate.objects.all()
    dic['cates']=cates
    return render(request,'goods_info/index.html',dic)

@decrotors.login
def goodsType(request,dic):
	return render(request,'goods_info/list.html',dic)

@decrotors.login
def detail(request,dic):
	return render(request,'goods_info/detail.html',dic)

def exit(request):
    del request.session['userName']
    return redirect(reverse('goods_info:index'))

@decrotors.login
def saveGoodsID(request,dic):
    if request.method =='POST':
        ID = int(request.POST['goodsID'])    
        userName = dic['userName']
        userID = user_info.objects.get(name=userName).pk
        goodsIDSet =  recent_views.objects.filter(goods_id_id=ID).filter(user_id_id=userID)
        if(len(goodsIDSet)>0):
            # 仅仅更新时间
            goodsIDSet[0].save()
        else:
            info = recent_views(goods_id_id=ID,user_id_id=userID)
            info.save()
        return HttpResponse(json.dumps({'isUpdated':1}))





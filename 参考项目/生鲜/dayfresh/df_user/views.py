# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from hashlib import sha1
import json
from models import *
from df_goods.models import *
from df_order.models import *
import login_check
from django.core.paginator import Paginator,Page


def register(req):
    titile = {'title': '天天生鲜-注册页面'}
    return render(req, 'df_user/register.html', titile)

def register_handle(req):
    print req
    if req.method == 'POST':
        post = req.POST
        uname = post.get('user_name')
        upwd = post.get('pwd')
        uemail = post.get('email')
        s1 = sha1()
        s1.update(upwd)
        upwd0 = s1.hexdigest()

        user = UserInfo()
        user.uname = uname
        user.upwd = upwd0
        user.uemail = uemail
        user.save()

        return redirect('/user/login/')
    return redirect('/user/register/')

def register_exist(req):
    name = req.GET.get('user_name', None)
    email = req.GET.get('email', None)
    if name:
        count0 = UserInfo.objects.filter(uname=name).count()
        tmp0 = json.dumps({'count': count0})
        return HttpResponse(tmp0)
    elif email:
        count1 = UserInfo.objects.filter(uemail=email).count()
        tmp1 = json.dumps({'count': count1})
        return HttpResponse(tmp1)

def login(req):
    uname = req.COOKIES.get('uname', '')
    context = {
        'title': '天天生鲜-登录页面',
        'error_name': 0,
        'error_pwd': 0,
        'uname': uname,
    }
    return render(req, 'df_user/login.html', context)

def login_handle(req):
    post = req.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    remember = post.get('remember')
    user = UserInfo.objects.filter(uname=uname)
    if len(user):
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest() == user[0].upwd:
            # Redirect不能设置Cookie，所以引入HttpResponse的子类HttpResponseRedirect
            red = HttpResponseRedirect('/')
            if remember == 1:
                red.set_cookie('uname', uname)
            else:
                # max_age=-1表示Cookie立即失效
                red.set_cookie('uname', '', max_age=-1)
            req.session['user_id'] = user[0].id
            req.session['user_name'] = uname
            return red
        else:
            context = {
                'title': '天天生鲜-登录页面',
                'error_name': 0,
                'error_pwd': 1,
                'uname': uname,
                'upwd': upwd,
            }
            return render(req, 'df_user/login.html', context)
    else:
        context = {
            'title': '天天生鲜-登录页面',
            'error_name': 1,
            'error_pwd': 0,
            'uname': uname,
            'upwd': upwd,
        }
        return render(req, 'df_user/login.html', context)

def logout(req):
    req.session.flush()
    return redirect('/')

@login_check.login
def info(req):
    user_email = UserInfo.objects.get(id=req.session['user_id']).uemail
    address = UserAddress.objects.filter(user=req.session['user_id'])
    if address.count() == 0:
        user_phone = ''
        user_address = ''
    else:
        user_phone = address[0].uphone
        user_address = address[0].uaddress
    goods_ids = req.COOKIES.get('goods_ids', '')
    goods_id_list = goods_ids.split(',')
    goods_list = []
    if goods_id_list[0] != '':
        for goods_id in goods_id_list:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    context = {
        'title': '天天生鲜-用户中心',
        'subtitle': '用户中心',
        'user_name': req.session['user_name'],
        'user_email': user_email,
        'user_phone': user_phone,
        'user_address': user_address,
        'goods_list': goods_list,
    }
    return render(req, 'df_user/user_center_info.html', context)

@login_check.login
def order(req, pindex):
    order_list = OrderInfo.objects.filter(user_id=req.session['user_id']).order_by('-oid')
    paginator = Paginator(order_list,  2)
    if pindex == '':
        pindex = '1'
    page = paginator.page(int(pindex))
    context = {'title': '天天生鲜-用户中心',
               'subtitle': '用户中心',
               'paginator': paginator,
               'page': page,
               }
    return render(req, 'df_user/user_center_order.html', context)

@login_check.login
def site(req):
    tmp = UserAddress.objects.filter(user=req.session['user_id'])
    address = UserAddress() if tmp.count()==0 else tmp[0]
    if req.method == 'POST':
        post = req.POST
        address.ureceiver = post.get('ureceiver')
        address.uaddress = post.get('uaddress')
        address.upostcode = post.get('upostcode')
        address.uphone = post.get('uphone')
        address.user_id = req.session['user_id']
        address.save()
    context = {'title': '天天生鲜-用户中心', 'subtitle': '用户中心', 'address': address}
    return render(req, 'df_user/user_center_site.html', context)

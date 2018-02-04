# coding=utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse
from models import user_info
from login.models import user_info
from django.core.urlresolvers import reverse 
import json
from person_info.toolKit import to_md5

def registe(request):	
	return render(request,'login/register.html')

def registHandler(request):
	name = request.POST['name']
	userInfo = user_info.objects.get(name=name)
	if name==userInfo.name:
		flag = {'flag':1}
	else:
		flag = {'flag':0}
	return HttpResponse(json.dumps(flag))

def saveDataHandler(request):
	uuserName= request.POST['user_name']
	upasswd = to_md5(str(request.POST['pwd']))
	uemail = request.POST['email']
	user = user_info(name=uuserName,passwd=upasswd,email=uemail)
	user.save()
	return redirect(reverse('login:login'))


def login(request):
	error_msg=request.session.get('error',default='')
	return render(request,'login/login.html',{'error':error_msg})

def loginHandler(request):
	if request.method == 'POST':
		userName = request.POST['username']
		passwd = to_md5(str(request.POST['pwd']))
		userInfo = user_info.objects.get(name=userName)
		if userInfo and userInfo.name == userName and userInfo.passwd == passwd:
			request.session.set_expiry(0)
			request.session['userName'] = userName		
			return redirect(reverse('goods_info:index'))
		else:
			request.session['error']=u'用户名或密码有误'
			request.session.set_expiry(1)		
			return redirect(reverse('login:login'))






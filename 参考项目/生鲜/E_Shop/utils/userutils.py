#! /usr/bin env python3
# -*- coding:utf-8 -*-

from User.models import *
from utils.commonutils import *


# 用户操作工具类
class UserCenter():

    # 用户操作分发器
    def user_dispath(self, request, *args, **kwargs):

        # 用户所能允许的操作
        user_method_allowed = ['login', 'register']

        # 当前用户的操作
        user_method = request.POST.get('type', '').lower()
        if user_method in user_method_allowed:
            handler = getattr(self, user_method, self.user_method_not_allowed)
        else:
            handler = self.user_method_not_allowed
        return handler(request, *args, **kwargs)

    # 当用户操作不被允许时
    def user_method_not_allowed(self, request, *args, **kwargs):
        pass

    # 序列化
    def serialize(self, obj):
        d = {}
        for k, v in obj.__dict__.items():
            d[k] = str(v)
        return d

    # 登陆
    def login(self, request, *args, **kwargs):
        timestamp = request.POST.get('time')
        import time
        current_server_time = time.time()*1000
        if not (current_server_time - 1000*60*10 <= int(timestamp) <= current_server_time):
            return
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.get(user=username)
            user_password = md5_check(user.password+str(timestamp))
            if user_password == password:
                request.session['user'] = self.serialize(user)
                return user
            else:
                request.session['loginError'] = u'密码不匹配'
                request.session['errorType'] = 'loginError'
                return None
        except Exception :
            err = User.UserNotFoundException()
            request.session['loginError'] = str(err.message)
            request.session['errorType'] = 'loginError'
            return None

    # 注册
    def register(self, request, *args, **kwargs):
        try:
            username = kwargs['username']
            password = kwargs['password']
            user = User.register(username, password)
            request.session['user'] = self.serialize(user)
            return user
        except User.UserExistException as err:
            request.session['registerError'] = str(err.message)
            request.session['errorType'] = 'registerError'
            return None

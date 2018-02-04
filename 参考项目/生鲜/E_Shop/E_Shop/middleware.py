# /usr/bin env python3
# -*- coding:utf-8 -*-
from django.http.response import HttpResponseRedirect
from E_Shop import settings
from django.http.request import HttpRequest
import re


class UserAuth(object):
    """
    用户未登录时，禁止访问用户中心及用户地址页面
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        """
            ---> 响应前的处理
            ---> 响应处理 self.get_response(request)
            ---> 响应后处理
        """
        if request.path in settings.AUTH:
            user = request.session.get('user', '')
            if not user:
                # 用户未登录重定向
                return HttpResponseRedirect('/user/login/')
        # 正常访问
        return self.get_response(request)

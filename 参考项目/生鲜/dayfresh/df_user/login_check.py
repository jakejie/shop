# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect


def login(func):
    def login_fun(req, *args, **kwargs):
        if req.session.has_key('user_id'):
            return func(req, *args, **kwargs)
        else:
            return HttpResponseRedirect('/user/login/')
    return login_fun

'''
http://127.0.0.1:8000/index?type=10
request.path: 表示当前路径，为‘/index/’；
request.get_full_path(): 表示完整路径，为‘/index?type=10’
'''
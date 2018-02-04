#-*-coding:utf-8-*-
import re
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from utils.wrappers import *
from .models import *


# 检查注册参数
def check_register_param(request):
    username = post(request, 'user_name')
    userpwd = post(request, 'user_pwd')
    usercpwd = post(request, 'user_cpwd')
    usermail = post(request, 'user_mail')
    flag = True
    # 判断用户名长度
    if not (5 <= len(username) <= 20):
        flag = False
        add_message(request, 'user_name', '用户名不在5~20之间!')
    # 判断用户密码长度
    if not (8 <= len(userpwd) <= 20):
        flag = False
        add_message(request, 'user_pwd', '用户密码不在8~20之间!')
    # 判断邮箱是否符合格式
    regex = '^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$'
    if not re.match(regex, usermail):
        flag = False
        add_message(request, 'user_mail', '用户密码不符合邮箱格式!')
    # 判断两次密码是否一致
    if userpwd != usercpwd:
        flag = False
        add_message(request, 'user_pwd', '两次密码不一致!')
    # 判断用户名是否存在
    if User.objects.user_by_username('user_name'):
        flag = False
        add_message(request, 'user_name', '用户名已经存在!')
    return flag


# 检查用户名是否存在
def username_exists(request):
    username = get(request, 'username')
    return User.objects.user_by_username(username)


# 检查登录参数是否存在
def check_login_params(request):
    username = post(request, 'user_name')
    userpwd = post(request, 'user_pwd')
    flag = True
    # 判断用户名长度
    if not (5 <= len(username) <= 20):
        flag = False
    # 判断用户密码长度
    if not (8 <= len(userpwd) <= 20):
        flag = False
    # 判断用户名是否存在
    user = User.objects.user_by_username(username)
    if not user:
        flag = False
    else:
        if user.user_pwd != password_encryption(userpwd):
            flag = False
    return flag


# 记住用户名
def reme_username(request, response):
    # 判断是否记住用户名
    reme = post(request, 'user_reme')
    if reme:
        set_cookie(response, 'user_name', post(request, 'user_name'))


# 保持登录状态
def keep_status_online(request):
    user = User.objects.user_by_username(username=post(request, 'user_name'))
    set_session(request, 'user_name', user.user_name)
    set_session(request, 'uid', user.id)


# 获取登录之前的url
def get_redirect_url(request):
    # 获得url
    url = get_cookie(request, 'pre_url')
    if not url:
        url = reverse('users:user_center_info')
    return url


# 判断用户是否登录状态
def user_is_online(request):

    return get_session(request, 'user_name')


# 用户身份验证
def check_user_login(func):
    def wrapper(request, *args, **kwargs):
        if user_is_online(request):
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('users:login'))
    return wrapper


# 检查地址数据
def check_site_params(request):
    userrecv = post(request, 'user_recv')
    useraddr = post(request, 'user_addr')
    usercode = post(request, 'user_code')
    userphone = post(request, 'user_phone')
    if len(userrecv) == 0:
        return False
    if len(useraddr) == 0:
        return False
    if len(usercode) != 6:
        return False
    if len(userphone) != 11:
        return False
    return True


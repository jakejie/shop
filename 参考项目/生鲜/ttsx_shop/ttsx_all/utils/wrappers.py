#-*-coding:utf-8-*-
import hashlib
from django.contrib import messages


# post
def post(request, key):
    return request.POST.get(key, '').strip()


# post_list
def post_list(request, key):
    return request.POST.getlist(key)


# get
def get(request, key):
    return request.GET.get(key, '').strip()


# set cookie
def set_cookie(response, key, value):
    response.set_cookie(key, value, max_age=60*60*24)


# get cookie
def get_cookie(request, key):
    return request.COOKIES.get(key, '')


# del cookie
def del_cookie(response, key):
    response.delete_cookie(key)


# set session
def set_session(request, key, value):
    request.session[key] = value


# get session
def get_session(request, key):
    return request.session.get(key, '')


# del session
def del_session(request):
    request.session.flush()


# 密码加密
def password_encryption(password, salt=''):
    sha = hashlib.sha256()
    new_password = 'nbcnhadscvgvacgv' + password + 'cbmhacvgvagZcv' + salt
    sha.update(new_password.encode('utf-8'))
    return sha.hexdigest()


# 定义消息的格式
# add_message
def add_message(request, key, value):
    message = key + ':' + value
    messages.add_message(request, messages.INFO, message)


# def get_messages
def get_messages(request):
    message = messages.get_messages(request)
    info = dict()
    for item in message:
        tmp = str(item).split(':')
        info[tmp[0]] = tmp[1]
    return info

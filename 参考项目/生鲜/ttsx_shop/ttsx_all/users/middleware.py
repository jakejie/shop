#-*-coding:utf-8-*-
from django.core.urlresolvers import reverse
from utils.wrappers import *


# 记录url中间件
class RecordUrlMiddleware(object):
    def process_response(self, request, response):
        exclude_url = [
            reverse('users:user_center_info'),
            reverse('users:register'),
            reverse('users:register_handle'),
            reverse('users:register_check_username'),
            reverse('users:login'),
            reverse('users:login_handle'),
            reverse('users:logout'),
            reverse('users:user_center_site'),
            reverse('users:user_center_order'),
            reverse('index'),
        ]
        if request.path not in exclude_url and response.status_code == 200:
            set_cookie(response, 'pre_url', request.get_full_path())
        return response

from django.db import models

from db.AbstractModel import AbstractModel
from utils.wrappers import *


# 用户管理类
class UserManager(models.Manager):
    # 判断用户名字是否存在
    def user_by_username(self, username):
        try:
            return self.get(user_name=username)
        except User.DoesNotExist:
            return None

    # 数据入库
    def user_register_save(self, request):
        user = User()
        user.user_name = post(request, 'user_name')
        # 密码加密
        user.user_pwd = password_encryption(post(request, 'user_pwd'))
        user.user_mail = post(request, 'user_mail')
        user.save()

    # 地址数据入库
    def user_site_save(self, request):
        user = self.user_by_username(get_session(request, 'user_name'))
        user.user_recv = post(request, 'user_recv')
        user.user_addr = post(request, 'user_addr')
        user.user_code = post(request, 'user_code')
        user.user_phone = post(request, 'user_phone')
        user.save()


# 用户模型
class User(AbstractModel):
    # 用户名
    user_name = models.CharField(max_length=30)
    # 用户密码
    user_pwd = models.CharField(max_length=70)
    # 用户邮箱
    user_mail = models.CharField(max_length=50)
    # 用户电话
    user_phone = models.CharField(max_length=11)
    # 用户地址
    user_addr = models.CharField(max_length=50)
    # 邮政编码
    user_code = models.CharField(max_length=10)
    # 收件人
    user_recv = models.CharField(max_length=20)

    # 自定义管理类
    objects = UserManager()

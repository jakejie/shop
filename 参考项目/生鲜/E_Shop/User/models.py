from django.db import models

# Create your models here.


# 用户
class User(models.Model):
    user = models.CharField(max_length=254, unique=True)
    password = models.CharField(max_length=255)

    class Meta(object):
        db_table = 'user_user'

    # 用户已存在异常
    class UserExistException(Exception):
        message = '用户已存在'

        def __init__(self):
            self.message = '用户已存在'

    # 用户未发现异常
    class UserNotFoundException(Exception):
        message = '用户不存在'

        def __init__(self):
            self.message = '用户不存在'

    # 用户注册
    @classmethod
    def register(cls, username, password, *args, **kwargs):
        try:
            return cls.objects.create(user=username, password=password)
        except Exception:
            raise User.UserExistException()

    # 用户登陆
    @classmethod
    def login(cls, username, password, *args, **kwargs):
        try:
            return cls.objects.get(user=username, password=password)
        except Exception:
            raise User.UserNotFoundException()

    def __str__(self):
        return u'%s%s' % (self.user, self.password)


class Address(models.Model):
    province = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    area = models.CharField(max_length=10)
    details = models.CharField(max_length=520)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    user = models.ForeignKey(User)
    isDelete = models.BooleanField(default=False)
    # 默认收货地址
    isPrimary = models.BooleanField(default=False)

    class Meta(object):
        db_table = 'user_address'

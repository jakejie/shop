#! /usr/bin env python3
# -*- coding:utf-8 -*-
from django.db import models
from User.models import User


# Create your models here.
class Order(models.Model):
    # 给程序看的uuid
    sign = models.CharField(max_length=120)
    # 时间+第几个订单 2017112715320001
    order = models.CharField(max_length=120)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=120)
    # 存储字符串
    orderitems = models.CharField(max_length=520)
    created = models.DateTimeField(auto_now_add=True)
    payway = models.CharField(max_length=10)
    status = models.CharField(max_length=20, default='待支付')
    trade_no = models.CharField(max_length=120, null=True, blank=True)


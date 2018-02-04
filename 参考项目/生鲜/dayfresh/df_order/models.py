# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class OrderInfo(models.Model):
    oid = models.CharField(max_length=20, primary_key=True)
    odate = models.DateTimeField(auto_now=True)
    oIsPay = models.BooleanField(default=False)
    ototal = models.DecimalField(max_digits=8, decimal_places=2)
    oaddress = models.CharField(max_length=150)
    user = models.ForeignKey('df_user.UserInfo')

class OrderDetailInfo(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    count = models.IntegerField()
    goods = models.ForeignKey('df_goods.GoodsInfo')
    order = models.ForeignKey('OrderInfo')
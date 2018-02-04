#! /usr/bin env python3
# -*- coding:utf-8 -*-

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


# 商品类别
class Category(models.Model):
    cname = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'shop_category'
        ordering = ['id']

    def __str__(self):
        return u'%s' % self.cname


# 商品颜色
class Color(models.Model):
    name = models.CharField(max_length=20)
    value = models.ImageField()

    class Meta:
        managed = False
        db_table = 'shop_color'

    def __str__(self):
        return u'%s%s' % (self.name, self.value)


# 商品信息
class Goods(models.Model):
    gname = models.CharField(max_length=255)
    gdesc = models.CharField(max_length=1024, blank=True, null=True)
    gprice = models.DecimalField(max_digits=10, decimal_places=2)
    goldprice = models.DecimalField(max_digits=10, decimal_places=2)
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='categoryId_id')  # Field name made lowercase.

    # 查询商品对应的图片
    def img(self):
        return self.store_set.first().color.value

    # 查询商品的所有颜色
    def color(self):
        return self.store_set.all()

    # 查询商品的型号
    def size(self):
        stores = StoreSize.objects.filter(store__goods__gname=self.gname)
        sizes = {}
        for store in stores:
            size = store.size.value
            size_id = store.size.id
            sizes[size_id] = size
        return sizes

    class Meta:
        managed = False
        db_table = 'shop_goods'

    def __str__(self):
        return u'%s' % self.gname


# 商品详情
class Goodsdetails(models.Model):
    value = models.ImageField()
    goodsid = models.ForeignKey(Goods, models.DO_NOTHING, db_column='goodsId_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'shop_goodsdetails'

    def __str__(self):
        return u'%s' % self.goodsid


# 商品大小
class Size(models.Model):
    value = models.CharField(max_length=255)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'shop_size'

    def __str__(self):
        return u'%s' % self.name


# 商品库存
class Store(models.Model):
    count = models.IntegerField()
    color = models.ForeignKey(Color, models.DO_NOTHING)
    goods = models.ForeignKey(Goods, models.DO_NOTHING)
    size = models.ManyToManyField(Size)  # 多对多

    class Meta:
        managed = False
        db_table = 'shop_store'

    def __str__(self):
        return u'%s%s%s' % (self.count, self.color, self.goods)


# 商品库存与商品型号
class StoreSize(models.Model):
    store = models.ForeignKey(Store, models.DO_NOTHING)
    size = models.ForeignKey(Size, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shop_store_size'
        unique_together = (('store', 'size'),)

    def __str__(self):
        return u'%s%s' % (self.store, self.size)



# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from tinymce.models import HTMLField


class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.ttitle.encode('utf8')

class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='df_goods/')
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    gunit = models.CharField(max_length=20)
    gclick = models.IntegerField()
    gintro = models.CharField(max_length=200)
    ginventory = models.IntegerField()
    gcontent = HTMLField()
    isDelete = models.BooleanField(default=False)
    gtype = models.ForeignKey('TypeInfo')
    def __str__(self):
        return self.gtitle.encode('utf8')
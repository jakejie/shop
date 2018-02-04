# -*- coding=utf-8 -*-
from django.db import models

# 用户信息表
class user_info(models.Model):
	name = models.CharField(max_length=50,unique=True)
	passwd = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=11,null=True,blank=True)
	registe_date = models.DateTimeField(auto_now=True)
	address = models.CharField(max_length=100,null=True,blank=True)

	def __unicode__(self):
		return self.name

	class Meta():
		db_table = 'user_info'

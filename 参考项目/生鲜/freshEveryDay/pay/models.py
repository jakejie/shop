# encoding=utf-8
from django.db import models

# 购物车表
class cart(models.Model):
	user_id = models.ForeignKey('login.user_info')
	goods_id = models.ForeignKey('goods_info.goods_info')
	buy_count = models.IntegerField()

	# 获取购物车所有商品
	def getGoods(self):
		return self.goods_info_set.all()


	class Meta():
		db_table = 'cart'

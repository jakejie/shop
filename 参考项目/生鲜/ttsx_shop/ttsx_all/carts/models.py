from django.db import models
# 公共模型类
from db.AbstractModel import AbstractModel


# 购物车管理类
class CartsManager(models.Manager):
    pass


# 购物车模型
class Carts(AbstractModel):
    # 购物车商品
    cart_goods = models.ForeignKey('goods.GoodsInfo')
    # 购物数量
    cart_amount = models.IntegerField(default=0)
    # 购物人
    cart_user = models.ForeignKey('users.User')

    objects = CartsManager()

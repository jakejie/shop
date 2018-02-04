from django.db import models

from goods.models import *
from User.models import *

# Create your models here.


class CartItemManager(models.Manager):
    def all(self):
        return super(CartItemManager, self).all().filter(isDelete=False)


class CartItem(models.Model):
    """
        isDelete=True 逻辑上已经删除。对上层调用不可见，该数据项不存在。
        isDelete=False 对于上层调用，该数据项存在。
    """
    goodsId = models.IntegerField()
    colorId = models.IntegerField()
    sizeId = models.IntegerField()
    count = models.IntegerField()
    username = models.ForeignKey(User, db_column='username_id')
    isDelete = models.BooleanField(default=False)

    objects = CartItemManager()

    def __str__(self):
        return u'goodsid:%s isDelete:%s' % (self.goodsId, self.isDelete)

    '''获得id对应的对象'''

    def goods(self):
        return Goods.objects.get(id=self.goodsId)

    def color(self):
        return Color.objects.get(id=self.colorId)

    def size(self):
        return Size.objects.get(id=self.sizeId)

    # 获得该购物项的总价
    def all_price(self):
        return self.goods().gprice*(int(self.count))

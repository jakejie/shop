from django.db import models

# Create your models here.


class CartInfo(models.Model):
    # 当需要引入别的应用的模块的字段作为外键时,用应用名.实体类名
    # 总之以 应用名. 来开头
    user = models.ForeignKey('df_user.UserInfo')
    goods = models.ForeignKey('df_goods.GoodsInfo')
    count = models.IntegerField()

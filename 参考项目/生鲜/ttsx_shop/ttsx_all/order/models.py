from django.db import models
from db.AbstractModel import *


# 订单商品详情  可能随着时间变更
class GoodsDetail(AbstractModel):
    # 商品名字
    goods_name = models.CharField(max_length=50)
    # 商品价格
    goods_price = models.IntegerField()
    # 商品图片
    goods_img = models.ImageField()
    # 商品数量
    goods_num = models.IntegerField()
    # 商品单位
    goods_unit = models.CharField(max_length=10)
    # 订单商品所属订单
    goods_order = models.ForeignKey('Order')


# 订单的基本信息表
class Order(AbstractModel):
    status = (
        (1, '待付款'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '已完成'),
    )
    pay = (
        (1, '货到付款'),
        (2, '微信支付'),
        (3, '支付宝支付'),
        (4, '银联支付'),
    )
    # 订单编号
    order_number = models.CharField(max_length=50)
    # 订单状态
    order_status = models.SmallIntegerField(choices=status, default=1)
    # 订单收货人
    order_recv = models.CharField(max_length=20)
    # 订单收货地址
    order_addr = models.CharField(max_length=50)
    # 收货人电话
    order_tele = models.CharField(max_length=11)
    # 订单所属用户
    order_user = models.ForeignKey('users.User')
    # 付款方式
    order_pay = models.SmallIntegerField(choices=pay, default=1)

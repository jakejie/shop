# from django.test import TestCase
# from .models import *
# import random
# import os
#
#
# # # 删除商品表
# # goods = GoodsInfo.objects.all()
# # goods.delete()
# #
# # # 删除商品分类表
# # cags = Category.objects.all()
# # cags.delete()
#
# # 插入商品分类表
# cags = ['新鲜水果', '海鲜水产', '猪牛羊肉', '禽类蛋品', '新鲜蔬菜', '速冻食品', ]
# for cag_info in cags:
#     cag = Category()
#     cag.cag_name = cag_info
#     cag.save()
#
#
# # 插入商品表
# units = ['500克', '1根', '1带', '200克', '5个', '1包', ]
# with open(os.path.abspath(os.path.curdir) + os.sep + 'data.txt', 'r', encoding='utf-8') as f:
#     for line in f:
#         # print(line[:-1])
#         goods = GoodsInfo()
#         goods.goods_name = line[:-1]
#         goods.goods_brief = '这是商品简介'
#         goods.goods_desc = '这是商品描述'
#         goods.goods_cag_id = random.randint(1, len(cags))
#         goods.goods_price = random.randint(1, 1000)
#         goods.goods_unit = units[random.randint(0, len(units)-1)]
#         goods.goods_image = 'images/goods/' + str(random.randint(1, 21)) + '.jpg'
#         goods.save()
#
#
# # 创建广告位数据
# for index in range(1, 5):
#     ads = Advertisement()
#     ads.ad_name = '广告位'
#     ads.ad_image = 'images/goods/ad/slide0' + str(index) + '.jpg'
#     ads.ad_link = '#'
#     ads.save()
#
#
# for index in range(1, 3):
#     ads = Advertisement()
#     ads.ad_name = '广告位'
#     ads.ad_image = 'images/goods/ad/adv0' + str(index) + '.jpg'
#     ads.ad_link = '#'
#     ads.save()

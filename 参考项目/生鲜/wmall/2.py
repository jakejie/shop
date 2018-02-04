#/!usr/local/env python
#coding=utf-8
#Model.py

from models.GoodsModel import GoodsModel

g = GoodsModel()
#rs = g.getOne('name,id,userid')
data = {
    'name':'21231',
}
rs = g.update(data,'id=1363')
print rs
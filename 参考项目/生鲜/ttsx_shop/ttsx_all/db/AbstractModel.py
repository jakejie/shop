#-*-coding:utf-8-*-
from django.db import models


# 定义公共的数据库类
class AbstractModel(models.Model):
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)
    # 是否逻辑删除
    is_delete = models.BooleanField(default=False)

    # 定义抽象类
    class Meta:
        abstract = True

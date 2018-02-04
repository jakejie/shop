from django.db import models
from tinymce.models import HTMLField
# 模型类全设计在这个文件下


class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle


class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    # 以后上传的图片资源统一存放在upload_to指定的目录下面
    # 同时上传文件还要在setting.py中配置一个media_root的
    gpic = models.ImageField(upload_to='df_goods')
    # max_digits表示共几位数  decimal_places 表示几位小数
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    isDelete = models.BooleanField(default=False)
    gunit = models.CharField(max_length=20, default='500g')
    gclick = models.IntegerField()
    gjianjie = models.CharField(max_length=200)
    gkucun = models.IntegerField()
    # 来自富文本编辑器 ,需要导模块,同时要在setting中配置
    gcontent = HTMLField()
    gtype = models.ForeignKey(TypeInfo)
    # gadv = models.BooleanField(default=False)

    def __str__(self):
        return self.gtitle

#  单价  单位   名称   图片   简介  介绍

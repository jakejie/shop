from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(TypeInfo)
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle']


@admin.register(GoodsInfo)
class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    # 只是在显示界面选择出现哪些内容,对增加商品时的字段并无影响
    list_display = ['id', 'gtitle', 'gprice', 'gunit', 'gclick', 'gkucun', 'gtype']


# admin.site.register(GoodsInfo)
# admin.site.register(TypeInfo)
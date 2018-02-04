# coding=utf-8
from django.contrib import admin
from login.models import *
from pay.models import *
from goods_info.models import *
from models import *

class user_info_inline(admin.StackedInline):
	model = user_info
	extra = 1


class goods_cate_inline(admin.StackedInline):
	model = goods_cate
	extra = 1


class goods_info_inline(admin.StackedInline):
	model = goods_info
	extra = 1


class recent_views_inline(admin.StackedInline):
	model = recent_views
	extra = 1


class order_inline(admin.StackedInline):
	model = orders
	extra = 1


class order_record_inline(admin.StackedInline):
	model = order_record
	extra = 1


class deli_address_inline(admin.StackedInline):
	model = deli_address
	extra = 1


class cart_inline(admin.StackedInline):
	model = cart
	extra = 1

@admin.register(user_info)
class user_info_admin(admin.ModelAdmin):
	list_display=['pk','name','passwd','email','phone_number','registe_date','address']
	inlines = [recent_views_inline,order_inline,deli_address_inline,cart_inline]


@admin.register(goods_cate)
class goods_cate_admin(admin.ModelAdmin):
	inlines=[goods_info_inline,]	
	list_display=['pk','name','img_url']


@admin.register(goods_info)
class goods_info_admin(admin.ModelAdmin):
	inlines=[recent_views_inline,cart_inline]	
	list_display=['pk','name','price','cate_id','stock','img_url','intro','desc','unit','sales_num','putaway_date']



@admin.register(recent_views)
class recent_views_admin(admin.ModelAdmin):
	list_display=['pk','goods_id','user_id','view_time']

@admin.register(orders)
class order_admin(admin.ModelAdmin):
	inlines = [order_record_inline]
	list_display=['pk','user_id','order_time','is_pay','deli_id','total_price']

@admin.register(order_record)
class order_record_admin(admin.ModelAdmin):
	list_display=['pk','order_id','goods_id','goods_count']

@admin.register(deli_address)
class deli_address_admin(admin.ModelAdmin):
	inlines = [order_inline]
	list_display=['pk','user_id','deli_name','detail_address','postcode','phone_number']

@admin.register(cart)
class cart_admin(admin.ModelAdmin):
	list_display=['pk','user_id','goods_id','buy_count']
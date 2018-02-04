#-*-coding:utf-8-*-
from django.template import Library
from django.core.urlresolvers import reverse
register = Library()


@register.filter
def myfilter(flag):
    contents = [
        {'name': '· 个人信息', 'link': reverse('users:user_center_info'), 'active': flag == 'info' and 'active' or ''},
        {'name': '· 全部订单', 'link': reverse('users:user_center_order'), 'active': flag == 'order' and 'active' or ''},
        {'name': '· 收货地址', 'link': reverse('users:user_center_site'), 'active': flag == 'site' and 'active' or ''},
    ]
    return contents


@register.filter
def order_by_update_time(queryset):
    goods_list = []
    for item in queryset:
        goods_list.append(item)
    goods_list.sort(key=lambda obj: obj.update_time, reverse=True)
    return goods_list

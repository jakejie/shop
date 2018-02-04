#-*-coding:utf-8-*-
from utils.wrappers import *
from .models import *
from carts.models import *


# 记录商品的浏览信息
def record_goods_browser(request):
    # 1.判断用户名和用户id是否存在
    username = get_session(request, 'user_name')
    userid = get_session(request, 'uid')
    if not(username and userid):
        return
    # 2.查询出浏览的商品id
    goodsid = get(request, 'id')
    # 3.保存浏览记录表
    try:
        # 3.1 已经存在，更新修改时间
        record = GoodsBrowse.objects.get(goods_name_id=goodsid, user_name_id=userid)
        record.save()
    except GoodsBrowse.DoesNotExist:
        # 3.2 不存在，插入数据
        records = GoodsBrowse.objects.filter(user_name_id=userid).order_by('update_time')
        # 3.2.1 当浏览记录小于5条时，进行插入
        if records.count() < 5:
            record = GoodsBrowse()
            record.goods_name_id = goodsid
            record.user_name_id = userid
            record.save()
        # 3.2.2 当浏览记录超过5条时，则修改时间最早记录的商品id并更新修改时间
        else:
            record = records[0]
            record.goods_name_id = goodsid
            record.save()


# 处理购物车总数显示
def get_total(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            # 用户存在，显示购物车总数
            user_id = Carts.objects.filter(cart_user_id=get_session(request, 'uid'))
            total = user_id.aggregate(models.Sum("cart_amount"))
            request.total = total['cart_amount__sum']
            if request.total is None:
                request.total = 0
        except ValueError:
            # 用户不存在，显示购物车总数为0
            request.total = 0
        finally:
            return view_func(request, *args, **kwargs)
    return wrapper

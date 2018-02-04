from django.shortcuts import render
from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import View
from utils.cartutils import *
from view.views import BaseRedirctView, BaseView

from utils.alipay import AliPay
from E_Shop.settings import BASE_DIR
import os


# 支付宝接口
alipay = AliPay(
    appid="2016082500310761",
    app_private_key_path=os.path.join(BASE_DIR, 'keys/app_private_key.txt'),
    alipay_public_key_path=os.path.join(BASE_DIR, 'keys/alipay_public_key.txt'),
    return_url="http://127.0.0.1:8000/order/alipay",
    app_notify_url='http://www.demonzero.pythonanywhere.com/alipay/post/'
)


# Create your views here.
class OrderView(View):
    def post(self, request):
        if request.session.get('user'):
            # 到订单界面
            # 购物项（订单）
            cartitems = request.POST.get('cartitems')
            # 重定向的问题
            request.session['cartitems'] = cartitems
            return HttpResponse('/order/orderlist/')
        else:
            return HttpResponse('/user/login/')


class OrderListView(BaseView):
    template_name = 'order.html'

    def get_extra_context(self, request, *args, **kwargs):
        raw_cartitems = request.session.get('cartitems', '')
        # del request.session['cartitems] 创建完成订单再删除
        cart_items = raw_cartitems.split(":")
        cart_manager = CartManager(request.session).cart_dispath()
        """
            根据商品，颜色，尺寸，数量获得订单项
            读取用户的默认收货地址
            如果创建订单成功，需不需要删除
        """
        order_items = []
        for cart_item in cart_items:
            order_items.append(cart_manager.get_cart_item(*cart_item.split(',')))
        user = request.session.get('user')
        # 该用户的默认收货地址
        address = User.objects.get(user=user['user']).address_set.first()
        all_price = 0
        for order_item in order_items:
            all_price += order_item.all_price()
        context = {'address': address, 'orderitems': order_items, 'allprice': all_price, 'raworderitems': raw_cartitems}
        return context


from order.models import *
from goods.models import *


class OrderCreatedView(BaseRedirctView):
    redirct_url = '' #我要支付的url

    # 事务
    def handle(self, request):
        request.session.modified = True
        del request.session['cartitems']
        # 删除购物记录
        orderitems = request.GET.get('orderitems')
        orderitems = orderitems.split(":")
        cart_manager = CartManager(request.session).cart_dispath()
        price = 0
        for orderitem in orderitems:
            """
                千万不要使用前端发来的数据，有可能中途被人恶意更改
            """
            price += cart_manager.get_cart_item(*orderitem.split(',')).all_price()

        for orderitem in orderitems:
            cart_manager.delete_cart_item(*orderitem.split(','))
        import time, uuid
        # order对象， （收货地址，订单项）（未付款，已付款，待发货，待收货，待评价，退货中，退货完成）
        order = Order.objects.create(name=request.GET.get('name'),
                                     phone=request.GET.get('phone'),
                                     address=request.GET.get('address'),
                                     payway=request.GET.get('type'),
                                     orderitems=orderitems,
                                     user=User.objects.get(user=request.session.get('user')['user']),
                                     sign=uuid.uuid4().hex,  # 基本上不会重复(订单的唯一标识)
                                     order=str(time.time()*1000),  # 很可能会重复(表示一个人在什么时间买的东西)
                                    )
        # 库存--
        for orderitem in orderitems:
            goodsId, colorId, sizeId, count = orderitem.split(',')
            store = Goods.objects.get(id=goodsId).store_set.filter(color_id=colorId)
            store = store.filter(size=Size.objects.get(id=sizeId)).first()
            store.count -= int(count)
            if store.count < 0:
                store.count = 0
            store.save()  # 保存到数据库
        # 根据支付方式，生成字符界面
        param = alipay.direct_pay(out_trade_no=order.sign,
                                  subject='九块九商城支付',
                                  total_amount=str(float('{:.2f}'.format(price))))
        url = 'https://openapi.alipaydev.com/gateway.do?'+param
        order.save()  # 未支付状态
        self.redirct_url = url


class AliPayView(View):
    def get(self, request):
        data = request.GET.dict()
        sign = data.pop('sign')
        if alipay.verify(data, sign):
            """
                取出订单对象，修改订单状态，添加trade_no(退款使用)(服务器和支付宝的一个交易凭证)
            """
            order = Order.objects.get(sign=data['out_trade_no'])
            order.status = '待发货'
            order.trade_no = data['trade_no']
            order.save()
            # 支付成功界面（让用户选择是否支付成功，跳到订单界面）
            # 重定向到订单界面
            return HttpResponse('支付成功')
        else:
            return HttpResponse('支付失败')

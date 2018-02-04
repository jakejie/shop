from django.shortcuts import render

from utils.cartutils import *
from goods.models import *
from view.views import *
from django.http.request import QueryDict

# Create your views here.


# 表单验证
from django import forms


class MyForm(forms.Form):
    goodsId = forms.IntegerField()
    colorId = forms.IntegerField()
    sizeId = forms.IntegerField()
    count = forms.IntegerField(required=False)

    def clean(self):
        super(MyForm, self).clean()
        data = self.cleaned_data
        # count = data['count']
        # if count < 0:
        #     self.errors['count'] = ['商品数量不能小于0']


class CartView(BaseRedirctView):
    """添加购物项， 重定向到购物车界面"""
    redirct_url = '/cart/cart.html'

    def handle(self, request, *args, **kwargs):
        request.session.modified = True

        cart_manager = CartManager(request.session).cart_dispath()
        cart_manager.add_cart_item(**request.POST.dict())


# 购物车相关操作
class GoodsCartView(BaseView, OperateView):
    template_name = 'cart.html'
    form_cls = MyForm

    def get_extra_context(self, request, *args, **kwargs):

        cart_manager = CartManager(request.session).cart_dispath()
        return {'cart': cart_manager.get_all_cart_items()}

    # 购物车中增加商品数量
    def add(self, request, goodsId, colorId, sizeId, *args, **kwargs):
        request.session.modified = True
        cart_manager = CartManager(request.session).cart_dispath()
        try:
            cart_manager.add_cart_item(goodsId=goodsId, colorId=colorId, sizeId=sizeId, count=1)
            return {"errorcode": 200, 'errormsg': ""}
        except Exception as e:
            return {"errorcode": -100, 'errormsg': str(e)}

    # 购物车中减少商品数量
    def min(self, request, goodsId, colorId, sizeId, *args, **kwargs):
        request.session.modified = True
        cart_manager = CartManager(request.session).cart_dispath()
        try:
            cart_manager.add_cart_item(goodsId=goodsId, colorId=colorId, sizeId=sizeId, count=-1)
            return {"errorcode": 200, 'errormsg': ""}
        except Exception as e:
            return {"errorcode": -100, 'errormsg': str(e)}

    # 删除购物车中的某项商品
    def delete(self, request, goodsId, colorId, sizeId, *args, **kwargs):
        request.session.modified = True
        cart_manager = CartManager(request.session).cart_dispath()
        try:
            cart_manager.delete_cart_item(goodsId=goodsId, colorId=colorId, sizeId=sizeId)
            return {"errorcode":200, "errormsg": ""}
        except Exception as err:
            return {"errorcode": -100, "errormsg": "删除失败"}


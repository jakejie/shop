#! /usr/bin env python3
# -*- coding:utf-8 -*-

from cart.models import *
from django.db.models import Q


class CartManagerObject(object):
    def add_cart_item(self, goodsId, colorId, sizeId, count, *args, **kwargs):
        pass

    def delete_cart_item(self, goodsId, colorId, sizeId, count, *args, **kwargs):
        pass

    def get_all_cart_items(self, *args, **kwargs):
        pass


class CartManager(CartManagerObject):
    """
        购物车管理分发类
        1. 如果用户已经登陆就返回使用数据库的购物车操作
        2. 如果用户未登陆就返回使用session的购物车操作
    """
    def __init__(self, session):
        self.session = session

    def cart_dispath(self):
        # 获取当前用户
        user_session = self.session.get('user', '')
        """
            如果用户已经登陆就将返回数据库操作的购物车管理器,
            否则返回session操作的购物车管理器
        """
        if user_session:
            cart_manager = DBCartManager(self.session)
        else:
            cart_manager = SessionCartManager(self.session)

        return cart_manager


# 当用户未登陆， 购物车信息存储到session中
class SessionCartManager(CartManagerObject):
    def __init__(self, session):
        self.session = session

    def add_cart_item(self, goodsId, colorId, sizeId, count, *args, **kwargs):
        # 构建商品信息并存入session
        context = {
            'goodsId': int(goodsId),
            'colorId': int(colorId),
            'sizeId': int(sizeId),
            'count': int(count),
        }

        # 获取用户信息，如果未登录使用临时用户身份。
        user_name = 'temporaryUser'

        # 获取session中当前用户的购物记录
        cart_session = eval(self.session.get(user_name, '[]'))

        # 如果购物车中已经有了相同商品，数量+1。否则，添加到购物车中。
        for cart_session_item in cart_session:
            if (int(cart_session_item['goodsId']) == context['goodsId'] and
                int(cart_session_item['colorId']) == context['colorId'] and
                int(cart_session_item['sizeId']) == context['sizeId']
                ):
                cart_session_item['count'] = int(cart_session_item['count']) + int(context['count'])
                break
        else:
            cart_session.append(context)

        # 将购物车容器存入session
        self.session[user_name] = str(cart_session)

    def delete_cart_item(self, goodsId, colorId, sizeId, *args, **kwargs):
        # 构建商品信息并进行数据清洗
        context = {
            'goodsId': int(goodsId),
            'colorId': int(colorId),
            'sizeId': int(sizeId),
        }

        # 获取用户信息，如果未登录使用临时用户身份。
        user_name = 'temporaryUser'

        # 获取session中当前用户的购物记录
        cart_session = eval(self.session.get(user_name, '[]'))

        # 如果购物车中已经有了相同商品，数量+1。否则，添加到购物车中。
        # 需要删除的购物车索引，若没查到=-1
        index = -1
        for cart_session_item in cart_session:
            if (int(cart_session_item['goodsId']) == context['goodsId'] and
                int(cart_session_item['colorId']) == context['colorId'] and
                int(cart_session_item['sizeId']) == context['sizeId']
                ):
                index = cart_session.index(cart_session_item)
                break

        if index != -1:
            del cart_session[index]

        # 将购物车容器存入session
        self.session[user_name] = str(cart_session)

    def get_all_cart_items(self, *args, **kwargs):

        # 获取当前用户
        user_session = self.session.get('user', '')
        if user_session:
            user_name = user_session['username']
        else:
            user_name = 'temporaryUser'

        # 获得购物车中的数据
        cart = eval(self.session.get(user_name, ''))

        # 将购物车中的存贮的id转变为响应的对象
        cart_object = []
        for cart_item in cart:
            cart_object.append({
                'goods': Goods.objects.get(id=cart_item['goodsId']),
                'color': Color.objects.get(id=cart_item['colorId']),
                'size': Size.objects.get(id=cart_item['sizeId']),
                'count': cart_item['count'],
            })

        return cart_object


# 当用户已登陆，购物车数据的变更在数据库中进行
class DBCartManager(CartManagerObject):
    def __init__(self, session):
        self.session = session

    # 往购物车中添加商品
    def add_cart_item(self, goodsId, colorId, sizeId, count, *args, **kwargs):
        # 构建商品信息并存入session
        context = {
            'goodsId': int(goodsId),
            'colorId': int(colorId),
            'sizeId': int(sizeId),
            'count': int(count),
        }

        # 获取用户信息
        user_session = self.session.get('user', '')
        user_name = str(user_session['user'])
        # context['username'] = user_name

        # 获取session中临时用户的存储信息
        contexts = []
        temporaryUser_cart_session = []
        if self.session.get('temporaryUser', '[]'):
            temporaryUser_cart_session = eval(self.session.get('temporaryUser', '[]'))
            flag = False
            for temporaryUser_cart_session_item in temporaryUser_cart_session:
                if (int(temporaryUser_cart_session_item['goodsId']) == context['goodsId'] and
                    int(temporaryUser_cart_session_item['colorId']) == context['colorId'] and
                    int(temporaryUser_cart_session_item['sizeId']) == context['sizeId']
                    ):
                    temporaryUser_cart_session_item['count'] = int(temporaryUser_cart_session_item['count']) \
                                                               + int(context['count'])
                    flag = True
                    continue
                else:
                    contexts.append(temporaryUser_cart_session_item)
            if not flag:
                contexts.append(context)

        # 获得该用户在数据库中的购物车集合
        user_name_id = User.objects.get(user=user_name).id
        cart_user = CartItem.objects.all().filter(username=user_name_id)
        cart = []
        if cart_user:
            for cart_user_item in cart_user:
                cart.append({
                    'goodsId': cart_user_item.goodsId,
                    'colorId': cart_user_item.colorId,
                    'sizeId': cart_user_item.sizeId,
                    'count': cart_user_item.count,
                })
        # 清空用户原购物车
        for cart_user_item in cart_user:
            cart_user_item.delete()
        """
            如果数据库中该用户的购物车不存在，且临时用户购物车存在。创建该用户的购物车。
            否则就判断：
                1. 数据库中该用户的购物集合中存在该商品，变更数量
                2. 数据库中不存在该商品，创建记录
        """
        if not temporaryUser_cart_session:
            if not cart:
                self._set_user([context], user_name)
                self.create_item(context)
            else:
                cart_union = self._union_cart(cart, [context])
                self._set_user(cart_union, user_name)
                for item in cart_union:
                    self.create_item(item)
        else:
            if not cart:
                self._set_user(contexts, user_name)
                for item in contexts:
                    self.create_item(item)
            else:
                cart_union = self._union_cart(cart, contexts)
                self._set_user(cart_union, user_name)
                for item in cart_union:
                    self.create_item(item)

        # 清空临时购物车
        if temporaryUser_cart_session:
            self.session['temporaryUser'] = ''

            # 查找购物车中的商品

    def search_cart_item(self, goodsId, colorId, sizeId, *args, **kwargs):
        # 构建商品信息并存入session
        context = {
            'goodsId': int(goodsId),
            'colorId': int(colorId),
            'sizeId': int(sizeId),
        }

        # 获取用户信息
        user_session = self.session.get('user', '')
        user_name = str(user_session['user'])
        context['username'] = user_name

        # 获得该用户在数据库中的购物车集合
        user_name_id = User.objects.get(user=user_name).id
        cart_user = CartItem.objects.all().filter(username=user_name_id)
        # 获取该商品
        goods_user = cart_user.filter(
            goodsId=context['goodsId'],
            sizeId=context['sizeId'],
            colorId=context['colorId']
        )

        return goods_user

    def get_cart_item(self, goodsId, colorId, sizeId, *args, **kwargs):
        goods_user = self.search_cart_item(goodsId, colorId, sizeId)
        return goods_user[0]

    # 从购物车中删除商品，逻辑删除，使isDelete=True
    def delete_cart_item(self, goodsId, colorId, sizeId, *args, **kwargs):
        # 查找购物车中的商品
        goods_user = self.search_cart_item(goodsId, colorId, sizeId)
        # 逻辑删除该商品
        goods_user.update(isDelete=1)

    def get_all_cart_items(self, *args, **kwargs):

        # 获取用户信息
        user_session = self.session.get('user', '')
        user_name = str(user_session['user'])

        # 获得该用户在数据库中的购物车集合
        user_name_id = User.objects.get(user=user_name).id
        cart_user = CartItem.objects.all().filter(username=user_name_id)
        cart = []
        for cart_user_item in cart_user:
            cart.append({
                'goodsId': cart_user_item.goodsId,
                'colorId': cart_user_item.colorId,
                'sizeId': cart_user_item.sizeId,
                'count': cart_user_item.count,
            })

        # 将购物车中的存贮的id转变为响应的对象
        cart_object = []
        for cart_item in cart:
            cart_object.append({
                'goods': Goods.objects.get(id=cart_item['goodsId']),
                'color': Color.objects.get(id=cart_item['colorId']),
                'size': Size.objects.get(id=cart_item['sizeId']),
                'count': cart_item['count'],
            })

        return cart_object

    @staticmethod
    def create_item(context):
        CartItem.objects.create(
            goodsId=context['goodsId'],
            colorId=context['colorId'],
            sizeId=context['sizeId'],
            count=context['count'],
            username=User.objects.get(user=context['username']),
        )

    @staticmethod
    def _union_cart(cart_user, cart_temporary):
        """

        :param cart_user: 用户在数据库中的购物车
        :param cart_temporary: 临时用户的购物车
        :return: 合并后的购物车
        :cart_temporary_item['flag']: 这件商品有没有在数据库中相同的
        """

        for cart_temporary_item in cart_temporary:
            cart_temporary_item['flag'] = False

        for cart_user_item in cart_user:
            for cart_temporary_item in cart_temporary:
                if (cart_user_item['goodsId'] == cart_temporary_item['goodsId'] and
                    cart_user_item['colorId'] == cart_temporary_item['colorId'] and
                    cart_user_item['sizeId'] == cart_temporary_item['sizeId']):
                        cart_user_item['count'] += cart_temporary_item['count']
                        cart_temporary_item['flag'] = True
                else:
                    continue

        for cart_temporary_item in cart_temporary:
            if not cart_temporary_item['flag']:
                cart_user.append(cart_temporary_item)

        return cart_user

    @staticmethod
    def _set_user(cart, username):
        for cart_item in cart:
            cart_item['username'] = username


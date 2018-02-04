#! /usr/bin env python3
# -*- coding:utf-8 -*-

# pip install pycrypto

from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from urllib.parse import quote_plus
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from base64 import decodebytes, encodebytes
import json


class AliPay(object):
    """
        创建支付对象，里面是常用的请求参数
    """
    def __init__(self, appid, app_notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):
        self.appid = appid
        self.app_notify_url = app_notify_url  # 异步通知
        self.return_url = return_url  # 同步通知
        self.app_private_key_path = app_private_key_path
        self.app_private_key = None

        # 加签
        with open(self.app_private_key_path) as fp:
            self.app_private_key = RSA.importKey(fp.read())

        # 验签
        self.alipay_public_key_path = alipay_public_key_path
        with open(self.alipay_public_key_path) as fp:
            self.alipay_public_key = RSA.importKey(fp.read())

        if debug is True:
            # 沙箱网关
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            # 正式网关
            self.__gateway = "https://openapi.alopay.com/gateway.do"

    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        # 直接支付
        # 业务参数
        biz_content = {
            "subject": subject,  # 这次交易的标题
            "out_trade_no": out_trade_no,  # uuid 订单号，只要是不重复就可以。appid下不能有重复的
            "total_amount": total_amount,  # 支付的金额
            "product_code": "FAST_INSTANT_TRADE_PAY",  # 交易的方式：即时到账
        }
        # 可以传入额外的参数，都更新到这个里面了
        biz_content.update(kwargs)
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        return self.sign_data(data)

    def build_body(self, method, biz_content, return_url=None):
        data = {
            "app_id": self.appid,
            "method": method,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }

        if return_url is not None:
            data["notify_url"] = self.app_notify_url
            data["return_url"] = self.return_url

        return data

    def sign_data(self, data):
        data.pop('sign', None)  # 删除sign
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)  # 排序，对字典排序
        # 待签名字符串
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        # 签名
        sign = self.sign(unsigned_string.encode("utf-8"))
        # 添加上''
        quote_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)

        # 获得最终的订单信息字符串
        signed_string = quote_string + "&sign=" + quote_plus(sign)
        return signed_string

    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)
        # 将字典类型的数据dump出来 针对biz-content
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, unsigned_string):
        # 开始计算签名
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))

        # base64 编码, 转换为unicode表示并移除回车
        sign = encodebytes(signature).decode("utf-8").replace("\n", "")
        return sign

    def direct_query(self, out_trade_no, trade_no):
        biz_content = {
            "out_trade_no":out_trade_no,
            "trade_no": trade_no,
        }
        data = self.build_body("alipay.trade.query", biz_content)
        return self.sign_data(data)

    def _verify(self, raw_content, signature):
        # 开始计算签名
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, decodebytes(signature.encode("utf8"))):
            return True
        return False

    def verify(self, data, signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)

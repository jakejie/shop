#!/usr/bin/env python
#coding: utf-8
'''
订单业务逻辑
'''
__author__ = 'Cui.D.H'

import sys, os, time, atexit, string
from signal import SIGTERM
from multiprocessing import Process
from time import sleep

class Order(Process):

    #self.db = MySQL()

    def run(self):
        # 死循环，进程不退出

        while True:
            print 'orders'
            time.sleep(300)


    def createOrder(self):
        print '创建订单'

    def createMgt(self):
        print '插入副表信息'


    def createLogistics(self):
        print '物流信息'

    def createShippingAddress(self):
        print '地址信息'

    '''
    修改商品库存
    '''
    def updateStock(self,type,number,goods_id,userid):
        if type == 1 :
            sql = "update wx_goods set stock = stock + %s WHERE id = %s AND userid= %s" % (number,goods_id,userid)
        else:
            sql = "update wx_goods set stock = stock - %s WHERE id = %s AND userid= %s" % (number,goods_id,userid)

        #开启事务
        self.db.query("START TRANSACTION")
        rs = self.db.query(sql)
        self.db.commit();
        return rs;


    '''
    创建订单信息验证
    '''
    def _validate(self):
        pass

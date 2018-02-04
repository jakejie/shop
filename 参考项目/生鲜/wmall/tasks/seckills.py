#!/usr/bin/env python
#coding: utf-8
'''
秒杀业务逻辑
'''
__author__ = 'Cui.D.H'
import sys, os, time, atexit, string
from signal import SIGTERM
from multiprocessing import Process
from time import sleep
from wmall.core.MySQL import MySQL

class Seckill(Process):
    def run(self):
        while True:
            data = {
                'userid'    : 2,
                'goods_id' :3,
                'seckill_id': 4,
                'openid'     :5,
                'number'     :6,
                'price'   : 7,
                'over_time' : time.time(),
            }
            #self.insertSeckillLog(data)
            print 'Seckill ' + time.ctime()
            sleep(5)

    def insertSeckillLog(self,data):
        db = MySQL()
        userid     = data['userid']
        goods_id   = data['goods_id']
        seckill_id = data['seckill_id']
        openid     = data['openid']
        number     = data['number']
        price      = data['price']
        over_time  = data['over_time']

        sql = 'insert into wx_seckill_log (userid,goods_id,seckill_id,openid,number,price,over_time) value (%s,%s,%s,%s,%s,%s,%s)' % (userid,goods_id,seckill_id,openid,number,price,over_time)
        return db.insert(sql)
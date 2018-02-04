#!/usr/bin/env python
#coding: utf-8
'''
超级表单导出并打包成zip
'''
__author__ = 'Cui.D.H'

import sys, os, time, atexit, string
import json
import urllib
from signal import SIGTERM
from multiprocessing import Process
from time import sleep
from wmall.core.MySQL import MySQL
from wmall.core.MyRedis import MyRedis



class Superform(Process):

    __db =  MySQL()
    __redis = MyRedis()
    __imgDir = '/mnt/hgfs/www/python/wmall/download/'

    def run(self):
        while True:
            lists = self.getSuperFormQueue()
            if lists:
                self.getFormDataLists(lists)

            print 'Superform ' + time.ctime()
            sleep(5)

    """
    从redis获取list
    """
    def getSuperFormQueue(self):
        sKey = 'superform_queue'
        lists = self.__redis.lpop(sKey)
        if lists:
            return json.loads(lists)


    """
    获取需要导出的数据
    """
    def getFormDataLists(self,lists):
        userid = lists['userid']
        formid = lists['formid']
        print userid + ' === ' + formid
        imgDir = userid +  '_' + formid
        self.getPic(imgur,imgDir)

    """
    查询图片信息
    """
    def getPicInfo(self,id):
        sql = "select * from pc_data where id = %s " % id
        print sql

    """
    下载图片保存到本地
    """
    def getPic(self,imgUrl,imgDir):
        imgDir = imgDir + '/'+ imgDir
        urllib.urlretrieve(imgUrl,imgDir)
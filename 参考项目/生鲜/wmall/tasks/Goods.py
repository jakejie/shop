#!/usr/bin/env python
#coding: utf-8
'''
商品业务逻辑
'''
__author__ = 'Cui.D.H'

import sys, os, time, atexit, string
import json
import urllib
from signal import SIGTERM
from time import sleep

from core.Tasks import Tasks
from core.Zip import Zip
from models.GoodsModel import GoodsModel
from models.PicDataModel import PicDataModel

class Goods(Tasks):

    __imgDir = '/mnt/hgfs/www/python/wmall/download/'
    __uploadUrl = 'http://t.pic.dodoca.com/'

    def run(self):
        while True:
            #获取队列
            lists = self.getGoodsQueue()
            if lists:
                #获取商品信息
                goodsInfo = self.getGoodsInfo(lists['goodsId'])
                userid = lists['userid']
                print goodsInfo
                picId = goodsInfo[0]
                if picId:
                    #获取图片信息
                    picInfo = self.getPicInfo(picId)
                    if picInfo:
                        for pic in picInfo:
                            imgUrl = pic[0]
                            if imgUrl:
                                filename = imgUrl.split('/')
                                filename = filename[-1]
                                #下载图片
                                self.getPic(imgUrl,filename,userid)
                        #图片打包
                        dirname = self.__imgDir + userid
                        zipfilename = dirname + '/' + userid + '.zip'
                        zip = Zip()
                        zip.zip_dir(dirname,zipfilename)

                print 'goods ' + time.ctime()
            else:
                print 'is not goods'
            sleep(5)

    """
    从redis获取list
    """
    def getGoodsQueue(self):
        redis = self.getRedis()
        sKey = 'goods_queue'
        lists = redis.lpop(sKey)
        if lists:
            return json.loads(lists)

    """
    从数据库获取商品信息
    """
    def getGoodsInfo(self,goodsId):
        gModel = GoodsModel()
        if goodsId:
            rs = gModel.getOne("pic_id",'id= %s' % goodsId )
            return rs
        else:
            return False

    """
    查询图片信息
    """
    def getPicInfo(self,id):
        pModel = PicDataModel()
        if id:
            rs = pModel.getOne("org",'id in (%s) ' % id )
            return rs
        else:
            return False

    """
    下载图片保存到本地
    """
    def getPic(self,imgUrl,filename,userid):
        if imgUrl:
            #判断文件目录是否存在
            if not os.path.exists(self.__imgDir + userid):
                os.makedirs(self.__imgDir + userid)
            imgDir = self.__imgDir + userid + '/' + filename
            imgUrl = self.__uploadUrl + imgUrl
            try:
                print imgUrl
                urllib.urlretrieve(imgUrl,imgDir)
            except:
                pass



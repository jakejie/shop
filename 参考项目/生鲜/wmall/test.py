#!/usr/bin/env python
#coding: utf-8


import sys, os, time, atexit, string
import json
import urllib
from signal import SIGTERM
from multiprocessing import Process
from time import sleep
from core.MySQL import MySQL
from core.MyRedis import MyRedis
from core.Zip import Zip

__db =  MySQL()

def getGoodsInfo(goodsId):
    __db =  MySQL()
    if goodsId:
        sql = "select pic_id from wx_goods where id = %s " % goodsId
        rs = __db.query(sql)
        return __db.fetchOneRow()
    else:
        return false


def getPicInfo(id):
    __db =  MySQL()
    if id:
        sql = "select org from pic_data where id in (%s)  " % id
        rs = __db.query(sql)
        return __db.fetchAllRows()
    else:
        return false

def getPic(imgUrl,filename):
    print imgUrl

    __imgDir = '/mnt/hgfs/www/python/wmall/download/'
    __uploadUrl = 'http://t.pic.dodoca.com/'
    if imgUrl:
        imgDir = __imgDir + filename
        imgUrl = __uploadUrl  + imgUrl
        urllib.urlretrieve(imgUrl,imgDir)





if __name__ == '__main__':

    dirname = '/mnt/hgfs/www/python/wmall/download'
    zipfilename = 'aa.zip'
    zip = Zip()
    rs = zip.zip_dir(dirname,zipfilename)

    print rs

    """
    goodsId = getGoodsInfo(1294)
    if goodsId:
        picInfo = getPicInfo(goodsId)
        if picInfo:
            for pic in picInfo:
                print pic[0]
                imgUrl = pic[0]
                if imgUrl:
                    filename = imgUrl.split('/')
                    filename = filename[-1]
                    print filename
                    getPic(imgUrl,filename)
    """
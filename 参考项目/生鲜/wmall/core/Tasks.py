#!/usr/bin/env python
#coding:utf-8

from multiprocessing import Process
from core.MyRedis import MyRedis

class Tasks(Process):

    __redis = ''

    def getRedis(self):
        if not self.__redis:
            self.__redis = MyRedis()
        return self.__redis
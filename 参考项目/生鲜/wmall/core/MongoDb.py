#!/usr/bin/python env
#coding:utf-8

'''
mongo conn 连接类
'''
import pymongo
from configs.settings import configs

class MongoDb:
    conn = None
    db = None
    commands = ''
    def __init__(self):
        try:
            self.connect(configs)
        except:
            print 'mongodb error'

    '''
    链接
    '''
    def connect(self,config):
        try:
            self.conn = pymongo.Connection(config['mongo']['dbhost'],config['mongo']['dbport'])
            self.db = self.conn[config['mongo']['dbname']]
        except:
            print 'mongodb 链接错误'


    '''
    获取自增id
    '''
    def getMongoAutoId(self,connection):
        commands = {"_id": connection}
        update= {
            "$inc":{
                    'count':1
                },
            }
        self.table = self.db[connection]
        rs = self.table.find_and_modify(commands,update,upsert=True)
        return rs['count']

    '''
    插入
    '''
    def insertData(self,tablename,data):
        #id = self.getMongoAutoId(tablename)
        if tablename and data:
            try:
                data['id'] = self.getMongoAutoId(tablename)
                self.table = self.db[tablename]
                result = self.table.insert(data)
            except:
                pass
        else:
            print 'insert data error'

    '''
    更新数据
    '''
    def updataData(self,tablename,where,data):
        if tablename and where and data:
            self.table = self.db[tablename]
            self.table.update(where,{'$set':data})
        else:
            pass

    '''
    查询数据
    '''
    def select(self,tablename,where):
        if tablename:
            self.table = self.db[tablename]
            if where:
                data = self.table.find(where)
            else:
                data = self.table.find()
            return data
        else:
            pass

    '''
    查询一条
    '''
    def find(self,tablename,where):
        if tablename:
            self.table = self.db[tablename]
            if where:
                data = self.table.find_one(where)
            else:
                data = self.table.find_one()
            return data
        else:
            pass

    '''
    总数
    '''
    def count(self,tablename,where):
        if tablename:
            self.table = self.db[tablename]
            if where:
                data = self.table.find(where).count()
            else:
                data = self.table.find().count()
            return data
        else:
            pass

    '''
    删除记录
    '''
    def remove(self,tablename,where):
        if tablename:
            self.table = self.db[tablename]
            if where:
                self.table.remove(where)
            else:
                self.table.remove()
        else:
            print 'talbe null'

    def close(self):
        return self.conn.disconnect()

    def getConn(self):
        return self.conn
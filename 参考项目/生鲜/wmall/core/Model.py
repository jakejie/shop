#/!usr/local/env python
#coding=utf-8
#Model.py
from core.MySQL import MySQL
import string
class Model:

    __primarykey = 'id'
    __count = 0
    __db = ''

    def __init__(self,table):
        self.table = table

    def getDb(self):
        if not self.__db:
            self.__db = MySQL()
        return self.__db

    """
    简单点，直接写条件
    """
    def getOne(self,fields = '*',where = '',order = ' id desc'):
        db = self.getDb()
        #where条件
        if where:
            where = ' where ' + where
        #order 条件
        if order:
            order = ' order by ' +order
        try:
            sql = 'select ' + fields + ' from ' + self.table + where + ' ' + order + ' limit 1 '
            rs = db.query(sql)
            if rs:
                return db.fetchOneRow();
            return rs
        except:
            return 'sql error'

    """
    获取列表
    """
    def lists(self,fields = '*',where = '' , order = ' id desc',page = 1 ,pageSize = 15):
        db = self.getDb()
        if where:
            where = ' where ' + where
        #order 条件
        if order:
            order = ' order by ' +order

        self.__count = self.count(where)
        if self.__count:
            start = pageSize * (page-1)
            try:
                sql = 'select ' + fields + ' from ' + self.table + where + ' ' + order + ' limit ' + str(start) + ' ,'+ str(pageSize)
                rs = db.query(sql)
                if rs:
                    return db.fetchAllRows()
                return rs
            except:
                return 'sql error2'
        else:
            return[]


    """
    插入数据
    """
    def insert(self,data):
        if data:
            column = ''
            value = ''
            for k,v in data.iteritems():
                column += k.strip() + ','
                value  += v.strip() + ','
            column = column.rstrip(',')
            value = value.rstrip(',')
            sql = "insert into " + self.table + "  (" + column + ") values (" + value + ")"
            db = self.getDb()
            try:
                insert_id = db.query(sql)
                return insert_id
            except:
                return 'error'
        else:
            return 'no data'

    """
    修改数据
    """
    def update(self,data,where = ''):
        if where:
            where = ' where ' + where
        if data:
            str = ''
            for k,v in data.iteritems():
                str += "`"+k.strip()+"`" + "='%s'," % v.strip()
            str = str.rstrip(',')
            sql = 'update ' + self.table + ' set ' + str + where
            db = self.getDb()
            try:
                db.update(sql)
                return db.getRowCount()
            except:
                return 'error'

        else:
            return 'no data'


    """
    删除数据
    """
    def delete(self,where = ''):
        if where:
            where = ' where ' + where
        sql = 'delete from ' + self.table + where
        db = self.getDb()
        try:
            db.query(sql)
            return db.getRowCount()
        except:
            return 'error'

    """
    获取总条数
    """
    def count(self,where = '',fields = '*'):
        db = self.getDb()
        if where:
            where = ' where ' + where
        if not fields:
            fields = self.__primarykey
        try:
            sql = 'select COUNT(' + fields + ') as total from ' + self.table + where + ' limit 1 '
            rs = db.query(sql)
            if rs:
                return db.fetchOneRow()
            return rs
        except:
            return 'sql error 1'


    """
    直接执行sql
    """
    def query(self,sql):
        if sql:
            try:
                rs = db.query(sql)
                if rs:
                    return db.fetchAllRows()
                return rs
            except:
                return 'error'
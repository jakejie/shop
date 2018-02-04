#coding=utf-8
 
import redis

from configs.settings import configs

class MyRedis:
 
    def __init__(self):
        self.dbhost = configs['redis']['dbhost']
        self.dbport = configs['redis']['dbport']
        self.dbname = configs['redis']['dbname']
        #self.r = redis.Redis(self.host, self.port, self.db)
        self.r = redis.Redis(host = self.dbhost, port = self.dbport, db = self.dbname)
    
    #1. strings 类型及操作
    #设置 key 对应的值为 string 类型的 value
    def set(self, key, value):
        return self.r.set(key, value)
 
    #设置 key 对应的值为 string 类型的 value。如果 key 已经存在,返回 0,nx 是 not exist 的意思
    def setnx(self, key, value):
        return self.r.setnx(key, value)
 
    #设置 key 对应的值为 string 类型的 value,并指定此键值对应的有效期
    def setex(self, key, time, value):
        return self.r.setex(key, time, value)
 
    #设置指定 key 的 value 值的子字符串
    #setrange name 8 gmail.com
    #其中的 8 是指从下标为 8(包含 8)的字符开始替换
    def setrange(self, key, num, value):
        return self.r.setrange(key, num, value)
 
    #获取指定 key 的 value 值的子字符串
    def getrange(self, key, start ,end):
        return self.r.getrange(key, start, end)
 
    #mget(list)
    def get(self, key):
        if isinstance(key, list):
            return self.r.mget(key)
        else:
            return self.r.get(key)
 
    #删除
    def remove(self, key):
        return self.r.delete(key)
 
    #自增
    def incr(self, key, default = 1):
        if (1 == default):
            return self.r.incr(key)
        else:
            return self.r.incr(key, default)
 
    #自减
    def decr(self, key, default = 1):
        if (1 == default):
            return self.r.decr(key)
        else:
            return self.r.decr(key, default)
 
    #2. hashes 类型及操作
    #根据email获取session信息
    def hget(self, email):
        return self.r.hget('session', email)
 
    #以email作为唯一标识，增加用户session
    def hset(self, email, content):
        return self.r.hset('session', email, content)
 
    #获取session哈希表中的所有数据
    def hgetall(self):
        return self.r.hgetall('session')
 
    #删除hashes
    def hdel(self, name, key = None):
        if(key):
            return self.r.hdel(name, key)
        return self.r.hdel(name)

    #清空当前db
    def clear(self):
        return self.r.flushdb()

    #清空所有数据库-慎用    
    def flushAll():
        return self.r.flushAll()

    #3、lists 类型及操作
    #适合做邮件队列
    #在 key 对应 list 的头部添加字符串元素
    def lpush(self, key ,value):
        return self.r.lpush(key, value)

    def rpush(self, key ,value):
        return self.r.rpush(key, value)    

    #从 list 的尾部删除元素,并返回删除元素
    def lpop(self, key):
        return self.r.lpop(key)

    def rpop(self, key):
        return self.r.rpop(key)

    #获取链表的元素个数
    def lSize(self,key):
        return self.r.llen(key)

    #返回链表中index位置的元素    
    def lGet(self,key, index):
        return self.r.lindex(key,index)

    #给链表中index位置的元素赋值    
    def lSet(self,key, index, value):
        return self.r.lset(key, index, value)

    #链表start至end之间的元素      
    def lRange(self,key, start = 0, end = -1):
        return self.r.lrange(key, start, end)
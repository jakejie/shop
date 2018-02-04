#coding=utf-8 
import time
from wmall.core.MySQL import MySQL
from wmall.core.MyRedis import MyRedis


'''
修改库存 
type 类型 1 增加
number 库存shul
goods_id 商品id
userid 用户id
'''
def updateStock(db,type,number,goods_id,userid):
    if type == 1 :
        sql = "update wx_goods set stock = stock + %s WHERE id = %s AND userid= %s" % (number,goods_id,userid)
    else:
        sql = "update wx_goods set stock = stock - %s WHERE id = %s AND userid= %s" % (number,goods_id,userid)

    #开启事务
    db.query("START TRANSACTION")
    rs = db.query(sql)
    db.commit();
    return rs;

'''
删除redis保存的库存数据
'''
def removeStockKey(r,id):
	sKey = 'seckill_stock_' + id
	return r.remove(sKey)

'''
根据秒杀id和openid查询用户是否已经存在秒杀记录
'''
def getBySeckillidAndOpenid(db,seckill_id,openid):
	if not seckill_id or not openid:
		return false
	else:
		sql = 'select id from wx_seckill_log where seckill_id = %s,openid = %s ' % (seckill_id,openid)
		return db.query(sql)

'''
用户秒杀成功从队列里面把记录写入秒杀记录表，前台调用秒杀记录验证是否秒杀成功
'''
def insertSeckillLog(db,data):
	userid     = data.userid
	goods_id   = data.goods_id 
	seckill_id = data.seckill_id
	openid     = data.openid 
	number     = data.number
	price      = data.price 
	over_time  = data.over_time 

	sql = 'insert into wx_seckill_log (userid,goods_id,seckill_id,openid,number,price,over_time) value (%s,%s,%s,%s,%s,%s,%s)' % (userid,goods_id,seckill_id,openid,number,price,over_time)
	return db.query(sql)	

'''
从redis获取list
'''
def getFromRedis(r,id):
	sKey = 'seckill_' + id
	return r.lpop(sKey)

'''
删除list
'''
def removeSeckillKey(r,id):
	sKey = 'seckill_' + id
	return r.remove(sKey)

''''
处理redis秒杀队列数据
1、从秒杀表查询正在进行的秒杀 状态为1 
2、获取通过seckillId和userid组成的list 
3、处理数据
'''
def seckill(db,r):
	sql = 'select id,userid,stock from wx_seckill where start_time < %s and status = 1 limit 0,20' % (time.time())
	db.query(sql)
	lists = db.fetchAllRows();
	if lists:
		for list in lists:
			#处理当前秒杀
			if list:
				#根据库存数据执行需要获取的队列记录数
				for x in xrange(1,list.stock):
					print x
					info = getFromRedis(r,list.id)
					#判断是在数据中已经存在
					exist = getBySeckillidAndOpenid(info.seckill_id,info.openid)
					#如果不存在则写入
					if not exist:
						insertSeckillLog(info)
						#修改库存
						updateStock(db,2,info.number,info.goods_id,info.userid)
					else:
						continue
				#如果处理结束则干掉当前的队列
				#干掉前端库存缓存
				removeStockKey(r,list.id)
				removeSeckillKey(r,list.id)			

			else:
				continue



if __name__ == '__main__':
	r = MyRedis()
	db = MySQL()
	seckill(db,r)
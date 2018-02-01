#-*- coding:utf-8 -*-
import sqlite3
def init_db():
    sqls = []
    sqls.append('create table if not exists customer (id  INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,password TEXT,email TEXT,sex TEXT,tel TEXT,address TEXT)')
    sqls.append('create table if not exists seller (id  INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,password TEXT,age INTEGER,sex TEXT,tel TEXT)')
    sqls.append('create table if not exists administrator (id  INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,password TEXT)')
    sqls.append('create table if not exists product (id  INTEGER PRIMARY KEY AUTOINCREMENT,type INT ,name TEXT,price TEXT,quantity INTEGER ,file_directory TEXT,des TEXT)')
    sqls.append('create table if not exists lineitem (item_id INTEGER PRIMARY KEY AUTOINCREMENT,production_id INT,quantity INT)')
    sqls.append('create table if not exists orders (order_id INTEGER PRIMARY KEY AUTOINCREMENT,order_list INT,item_id INT,user_id INT, status INT)')

    sqls.append("insert into customer VALUES (NULL ,'ruthy','rrr','ruthy@163.com','女','11111111','beijing')")
    sqls.append("insert into customer VALUES (NULL ,'jack','jjj','jack@163.com','男','11111111','shanghai')")
    sqls.append("insert into seller VALUES (NULL,'peter','ppp',45,'男','2222222222')")
    sqls.append("insert into seller VALUES (NULL,'john','jjj',41,'男','2222222222')")

    sqls.append("insert into product VALUES (NULL,0,'黑暗中的光','17.88',20,'1.jpg','this is a good book')")
    sqls.append("insert into product VALUES (NULL,0,'习近平谈治国理政','64',20,'3.jpg','this is a good book')")
    sqls.append("insert into product VALUES (NULL,0,'秘密','41.8',20,'5.jpg','this is a good book')")
    sqls.append("insert into product VALUES (NULL,0,'TensoFlow实战','64.9',20,'7.jpg','this is a good book')")

    sqls.append("insert into product VALUES (NULL,0,'菜与刀（精装珍藏版）','19.30',20,'10.jpg','this is a great book')")
    sqls.append("insert into product VALUES (NULL,0,'人类简史：从动物到上帝（新版）','40.8',20,'12.jpg','this is a great book')")
    sqls.append("insert into product VALUES (NULL,0,'未来简史','40.8',20,'13.jpg','this is a great book')")
    sqls.append("insert into product VALUES (NULL,0,'无人生还（精装纪念版）','31.6',20,'15.jpg','this is a great book')")
    sqls.append("insert into product VALUES (NULL,0,'东方快车谋杀案','23.4',20,'17.jpg','this is a great book')")

    sqls.append("insert into product VALUES (NULL,0,'Python编程从入门到实践','64.20',20,'18.jpg','this is a nice book')")
    sqls.append("insert into product VALUES (NULL,0,'AI：人工智能的本质与未来','41,10',20,'19.jpg','this is a nice book')")
    sqls.append("insert into product VALUES (NULL,0,'Python高性能编程','64.90',20,'9.jpg','this is a nice book')")
    sqls.append("insert into product VALUES (NULL,0,'Hadoop权威指南：大数据的存储与分析（第四版）','116.90',20,'20.jpg','this is a nice book')")

    sqls.append("insert into product VALUES (NULL,0,'新东方雅思词汇：乱序版','43.70',20,'21.jpg','this is a perfect book')")
    sqls.append("insert into product VALUES (NULL,0,'新版中日交流标准日本语','98.03',20,'22.jpg','this is a perfect book')")
    sqls.append("insert into product VALUES (NULL,0,'物演通论','95',20,'23.png','this is a perfect book')")

    sqls.append("insert into product VALUES (NULL,1,'Flash案例精华——视频教程全集','180',20,'24.png','this is a perfect book')")
    sqls.append("insert into product VALUES (NULL,1,'OpenStack最佳实践','52',20,'25.png','this is a perfect book')")
    sqls.append("insert into product VALUES (NULL,1,'在路上：公路音乐','50',20,'26.png','this is a perfect book')")
    sqls.append("insert into product VALUES (NULL,1,'过耳不忘','46',20,'27.png','this is a perfect book')")
    sqls.append("insert into product VALUES (NULL,1,'欧美永恒经典','89',20,'28.png','this is a perfect book')")



    for sql in sqls:
        conn = sqlite3.connect("easytao.db")
        cursor=conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

def query_IDcustomer(name):
	sql = "select id from customer where name='"+name+"'"
	conn = sqlite3.connect("easytao.db")
	cursor = conn.cursor()
	id = cursor.execute(sql)
	return id

def query_customer():
	sql = "select * from customer"
	conn = sqlite3.connect("easytao.db")
	cursor = conn.cursor()
	rows = cursor.execute(sql)
	list = []
	for row in rows:
		list.append(row)
	conn.commit()
	cursor.close()
	conn.close()
	return list

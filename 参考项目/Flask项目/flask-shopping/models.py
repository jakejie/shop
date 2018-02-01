import sqlite3

def get_conn():
    return sqlite3.connect("easytao.db")

# 用户类
class Customer(object):
    def __init__(self,user_id, user_name,user_password):
        self.user_id=user_id
        self.user_name=user_name
        self.password=user_password

    def add_to_basket(self,production_id,quantity=1):
        Sale.add_to_basket(self.user_id,production_id,quantity)
    @staticmethod
    def get_id_by_name(user_name):
        sql = "select id from customer where name='"+user_name+"'"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        for row in rows:
            my_id=row[0]
            conn.commit()
            cursor.close()
            conn.close()
            return my_id
    @staticmethod
    def is_valid(name,password):
        sql = "select * from customer"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        p=0
        for row in rows:
            if name==row[1] and password==row[2]:
                p = 1
                break
        conn.commit()
        cursor.close()
        conn.close()
        return p

    @staticmethod
    def get_id(name, password):
        sql = "select * from customer"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        for row in rows:
            if name == row[1] and password == row[2]:
                conn.commit()
                cursor.close()
                conn.close()
                return row[0]

    @staticmethod
    def if_name_is_repeated(name):
        sql = "select * from customer"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        p = 0
        for row in rows:
            if name == row[1]:
                p = 1
                break
        conn.commit()
        cursor.close()
        conn.close()
        return p

    def if_name_is_repeated_for_customer_manage(name):
        sql = "select * from customer where name!='"+ name + "'"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        p = 0
        for row in rows:
            if name == row[1]:
                p = 1
                break
        conn.commit()
        cursor.close()
        conn.close()
        return p

    @staticmethod
    def save_to_db(name, password, email, sex, tel, address):
        sql = "insert into customer VALUES (NULL,?,?,?,?,?,?)"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (name, password, email, sex, tel, address))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_to_db(user_id,name, password, email, sex, tel, address):
        sql = "update customer set name='"+str(name)+"',password='"+str(password)+"',email='"+str(email)+"',sex='"+str(sex)+"',tel='"+str(tel)+"',address='"+str(address)+"' where id="+str(user_id)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def search_id_by_name(name):
        sql = "select id from customer where name='"+name+"'"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        for row in rows:
            user_id=row[0]
            conn.commit()
            cursor.close()
            conn.close()
            return user_id

    @staticmethod
    def query_all():
        sql = "select * from customer"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        lists=[]
        for row in rows:
            lists.append(row)
        conn.commit()
        cursor.close()
        conn.close()
        return lists

    @staticmethod
    def query_all_by_id(id):
        sql = "select * from customer where id="+str(id)
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        list = []
        for row in rows:
            list.append(row)
        conn.commit()
        cursor.close()
        conn.close()
        return list

    @staticmethod
    def delete_customer(id):
        sql = "delete from customer where id=" + str(id)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def __str__(self):
        return 'id:{}--name:{}'.format(self.user_id,self.user_name)







class Seller(object):
    def __init__(self,user_id, user_name,user_password):
        self.user_id=user_id
        self.user_name=user_name
        self.password = user_password
    def is_valid(name,password):
        sql = "select * from seller"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        p=0
        for row in rows:
            if name==row[1] and password==row[2]:
                p = 1
                break
        conn.commit()
        cursor.close()
        conn.close()
        return p

    @staticmethod
    def search_id_by_name(name):
        sql = "select id from seller where name='" + name + "'"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        for row in rows:
            user_id = row[0]
            conn.commit()
            cursor.close()
            conn.close()
            return user_id

    @staticmethod
    def search_fullsub_by_id(id):
        sql = "select full_sub from seller where id="+str(id)
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        for row in rows:
            user_id = row[0]
            conn.commit()
            cursor.close()
            conn.close()
            return user_id
    @staticmethod
    def get_id_by_name(user_name):
        sql = "select id from seller where name='"+user_name+"'"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        for row in rows:
            my_id=row[0]
            conn.commit()
            cursor.close()
            conn.close()
            return my_id

    @staticmethod
    def query_all_by_id(id):
        sql = "select * from seller where id=" + str(id)
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        list = []
        for row in rows:
            list.append(row)
        conn.commit()
        cursor.close()
        conn.close()
        return list

    @staticmethod
    def query_seller_product(seller_id):
        sql="select product.* ,seller_product.discount,seller_product.full_sub from seller_product,product where product.id=seller_product.product_id and seller_product.on_sale=1 and seller_id="+str(seller_id)
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        list = []
        for row in rows:
            list.append(row)
        conn.commit()
        cursor.close()
        conn.close()
        return list

    @staticmethod
    def save_to_db(name, password, email, sex, tel,full_sub):
        sql = "insert into seller VALUES (NULL,?,?,?,?,?,?)"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (name, password, email, sex, tel,full_sub))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_seller(id):
        sql = "delete from seller where id=" + str(id)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_production(seller_id,product_id):
        sql = "update seller_product set on_sale=0 where seller_id=" + str(seller_id)+" and product_id="+str(product_id)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    @staticmethod
    def update_to_db(user_id, name, password, email, sex, tel):
        sql = "update seller set name='" + str(name) + "',password='" + str(password) + "',email='" + str(
            email) + "',sex='" + str(sex) + "',tel='" + str(tel) + "' where id=" + str(
            user_id)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def query_all():
        sql = "select * from seller"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        lists = []
        for row in rows:
            lists.append(row)
        conn.commit()
        cursor.close()
        conn.close()
        return lists

    @staticmethod
    def add_new_production(seller_id, product_id, discount, full_sub):
        sql = "insert into seller_product VALUES (NULL,?,?,?,?,1)"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (seller_id,product_id,discount,full_sub))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def change_production(seller_id, product_id,discount,full_sub):
        sql = "update seller_product set discount='"+str(discount)+"',full_sub='"+str(full_sub)+"' where seller_id=" + str(seller_id) + " and product_id=" + str(
            product_id)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def if_name_is_repeated_for_seller_manage(name):
        sql = "select * from seller where name!='"+ name + "'"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        p = 0
        for row in rows:
            if name == row[1]:
                p = 1
                break
        conn.commit()
        cursor.close()
        conn.close()
        return p

class Production(object):
    def __init__(self,production_id,type=None,name=None,description=None):
        self.production_id=production_id
        self.type=type
        self.name=name
        self.description=description

    @staticmethod
    def get_production_id(name):
        sql = "select id from product where name='"+str(name)+"'"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        for row in rows:
            id = row[0]
            conn.commit()
            cursor.close()
            conn.close()
            return id

    @staticmethod
    def get_onsale_by_production_id(id):
        sql = "select on_sale from seller_product where product_id=" + str(id)
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        for row in rows:
            on_sale = row[0]
            conn.commit()
            cursor.close()
            conn.close()
            # print("lallallallal")
            # print(on_sale)
            return on_sale
    @staticmethod
    def edit(id,type,name,price,quantity,image,des,type1):
        sql = "update product set type='"+str(type)+"',name='"+str(name)+"',price='"+str(price)+"',quantity="+quantity+",image='"+str(image) +"',des='"+str(des)+"',type1='"+str(type1)+" 'where id="+str(id)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    @staticmethod
    def add_new_production(type, name, price, quantity, image,des,type1):
        sql = "insert into product VALUES (NULL,?,?,?,?,?,?,?)"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(type,name,price,quantity,image,des,type1))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_production(id):
        sql = "delete from product where id="+str(id)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def query_by_type(type):
        sql = "select * from product where type ='"+str(type)+"'"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        list = []
        for row in rows:
            list.append(row)
        conn.commit()
        cursor.close()
        conn.close()
        return list

    def query_by_type_type1(type,type1):
        sql = "select * from product where type ='"+str(type)+"' and type1='"+str(type1)+"'"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        list = []
        for row in rows:
            list.append(row)
        conn.commit()
        cursor.close()
        conn.close()
        return list

    @staticmethod
    def all_query(order=None):
        if order:
            sql = "select * from product desc order by id "+order
        else:
            sql = "select * from product desc order by id"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        list = []
        for row in rows:
            list.append(row)
        conn.commit()
        cursor.close()
        conn.close()
        return list

    @staticmethod
    def query_product_by_id(product_id):
        sql = "select product.* ,seller_product.discount,seller_product.full_sub from seller_product,product where product.id=seller_product.product_id and product_id=" + str(
            product_id)
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        list = []
        for row in rows:
            list.append(row)
        conn.commit()
        cursor.close()
        conn.close()
        return list

    @staticmethod
    def basket_production_data(user_id):
        sql = " select orders.order_id,lineitem.item_id,lineitem.quantity,product.*,seller_product.discount,seller_product.full_sub,seller_id  from lineitem,orders,product,seller_product where lineitem.item_id=orders.item_id and lineitem.production_id=product.id and orders.status=0 and product.id=seller_product.product_id and orders.user_id=" + str(
            user_id)
        # order_id,item_id,quantity,production_id,type,name,price,description,file_directory
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        list = []
        for row in rows:
            list.append(row)

        conn.commit()
        cursor.close()
        conn.close()
        return list

    @staticmethod
    def order_production_data(user_id):
        sql = " select orders.order_list,lineitem.quantity,product.*  from lineitem,orders,product where lineitem.item_id=orders.item_id and lineitem.production_id=product.id and orders.status=1 and orders.user_id=" + str(
            user_id)
        # order_id,item_id,quantity,production_id,type,name,price,description,file_directory
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        list = []
        for row in rows:
            list.append(row)
        conn.commit()
        cursor.close()
        conn.close()
        return list


class Lineitem:
    def __init__(self,item_id,production_id,user_id,quantity):
        self.item_id = item_id
        self.production_id = production_id
        self.quantity = quantity
        self.p=Production(production_id=production_id)
    def get_production_name(self):
        return self.p.get_production_name()
    def get_sum(self):
        return self.p.get_production_price()*self.quantity

    @staticmethod
    def get_production_data(item_id):
        sql = "select production_id from lineitem where item_id=" + str(item_id)
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        for row in rows:
            production_id=row[0]
            conn.commit()
            cursor.close()
            conn.close()
            return Production.get_production_data(production_id)
    @staticmethod
    def get_order_list(user_id):
        sql = "select * from orders where user_id=" + str(user_id)+" and status=0"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        list=[]
        for row in rows:
            list.append(row)
        conn.commit()
        cursor.close()
        conn.close()
        return list


    @staticmethod
    def is_exist(production_id):
        sql = "select item_id from lineitem where production_id=" + str(production_id)
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        lists =[]
        for row in rows:
            lists.append(row[0])
        conn.commit()
        cursor.close()
        conn.close()
        return lists
    @staticmethod

    def get_production_id(item_id):
        sql = "select production_id from lineitem where item_id=" + str(item_id)
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)

        for row in rows:
            price = row[0]
            conn.commit()
            cursor.close()
            conn.close()
            return price
        return None
    @staticmethod
    def add_one(item_id):
        sql = "update lineitem set quantity = quantity+1 where item_id="+str(item_id)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

class Orders(object):
    def __init__(self,user_id):
        self.user_id=user_id
        sql = "select order_list,item_id from orders where user_id="+str(user_id)+"  and status =0"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)

        basket={}
        for row in rows:
            if row[0] in basket.keys():
                basket[row[0]].append(row[1])
            else:
                basket[row[0]]=[]
                basket[row[0]].append(row[1])

        conn.commit()
        cursor.close()
        conn.close()
        self.basket=basket

    def get_basket(self):
        return self.basket

    def get_max_order_list(self):
        sql = "select max(order_list) from orders where user_id=" + str(self.user_id)
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)

        for row in rows:
            max=row[0]
            conn.commit()
            cursor.close()
            conn.close()
            return max

    def checkout(self):
        max = self.get_max_order_list()
        sql = sql = "update orders set order_list = "+str(max+1)+" where user_id="+str(self.user_id)+" and status=0"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()



        sql = sql = "update orders set status = 1 where user_id="+str(self.user_id)+" and status=0"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()






    def add_item(self,user_id,production_id):
        sql = "select item_id  from lineitem join (select item_id as it,status from orders)  as t on (lineitem.item_id=t.it and t.status=0 and lineitem.production_id="+str(production_id)+")"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        p = 0
        for row in rows:
            if row[0]:
                Lineitem.add_one(row[0])
                p = 1
                break
        conn.commit()
        cursor.close()
        conn.close()

        if p==0:
            sql = "insert into lineitem VALUES (NULL,"+production_id+",1)"
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
###
###
            sql = "select item_id  from lineitem  where production_id="+str(production_id)+" order by item_id desc  "
            conn = get_conn()
            cursor = conn.cursor()
            rows = cursor.execute(sql)
            t=None
            for row in rows:
                t=row[0]
                conn.commit()
                cursor.close()
                conn.close()
                break;

            sql = "insert into orders VALUES (NULL,0,?,?,0)"
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute(sql, (t, user_id))
            conn.commit()
            cursor.close()
            conn.close()
    @staticmethod
    def delete_from_basket(order_id,item_id):
        sql = "delete from orders where order_id=" + str(order_id)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

        sql = "delete from lineitem where item_id=" + str(item_id)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def add_from_basket(item_id):
        sql = "update lineitem set quantity=quantity+1 where item_id=" + str(item_id)
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    def get_order_sum(order_list,user_id):
        sql = "select item_id  from orders  where order_list=" + str(order_list) + " and user_id="+str(user_id)
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        list=[]
        for row in rows:
            list.append(row[0])
        conn.commit()
        cursor.close()
        conn.close()
        sum=0

        for i in list:
            sql = "select lineitem.quantity,price from lineitem,production where production.production_id=lineitem.production_id and lineitem.item_id="+str(i)
            conn = get_conn()
            cursor = conn.cursor()
            rows = cursor.execute(sql)
            for row in rows:
                sum=sum+row[0]*row[1]
            conn.commit()
            cursor.close()
            conn.close()
        return sum

class Sale(object):
    def __init__(self,user_name):
        self.user_id=Customer.get_id_by_name(user_name)
    def checkout(self):
        o = Orders(self.user_id)
        o.checkout()

    def add_item(self,production_id):
        o = Orders(self.user_id)
        o.add_item(self.user_id, production_id)
    @staticmethod
    def get_product_price_total(basket_data):
        total = 0
        for data in basket_data:
            quantity = data[2]
            price = data[6]
            intem_total = float(quantity) * float(price)
            total = float(total) + float(intem_total)
        return total

    @staticmethod
    def get_price_discount(basket_data):
        discount_total = 0
        for data in basket_data:
            quantity = data[2]
            price = data[6]
            discount=data[11]
            intem_discount = float(quantity) * float(price)*float(1.00-float(discount))
            discount_total = float(discount_total) + float(intem_discount)
        return "%.2f" % discount_total

    @staticmethod
    def get_price_full_sub(basket_data):
        # print('&&&&&&&&&&&')
        sub_total = 0
        sub_a =0
        sub_b=0
        for data in basket_data:
            # print('KKKKKKKKKK')
            sell_id = data[13]
            quantity = data[2]
            price = data[6]
            if sell_id == 1:
                # print("@@@@@@@@@")
                a = Seller.search_fullsub_by_id(sell_id)
                if data[12] != '0':
                    b = a.split('-')[0]
                    c = a.split('-')[1]
                    # print(a,b,c)
                    sub_intem=float(quantity) * float(price)
                    sub_total=sub_total+sub_intem
                    sub_a=Sale.sub(sub_total,b,c)
                    # print(sub_a)
                else:
                    sub_a=0.0
                # print(sub_a)
            elif sell_id==2:
                a = Seller.search_fullsub_by_id(sell_id)
                if data[12] != '0':
                    b = a.split('-')[0]
                    c = a.split('-')[1]
                    # print(sub_total,b,c)
                    sub_intem = float(quantity) * float(price)
                    sub_total = sub_total + sub_intem
                    sub_b = Sale.sub(sub_total, b, c)
                else:
                    sub_b=0.0
                # print(sub_b)
        return sub_a+sub_b


    @staticmethod
    def sub(total,b,c):
        sub_all=0.0
        total1=float(total)
        b1=float(b)
        c1=float(c)
        if total1:
            while(total1>b1):
                sub_all=sub_all+c1
                total1=total1-b1
            return sub_all
        else:
            return 0


    @staticmethod
    def add_to_basket(user_id,production_id):
    #return the item_id
        order = Orders(user_id)
        basket = order.get_basket()
        for b in basket.keys():
            lit = basket[b]
            for i in lit:
                if Lineitem.get_production_id(i)==production_id:
                    return 1
        Orders.add_item(user_id,production_id)
        return 1
        # order.add_item(user_id,production_id)





class System(object):
    @staticmethod
    def query_basket_production_data_by_user_id(user_id):
        return Production.basket_production_data(user_id)

class Administrator(object):
    def __init__(self,user_id, user_name,user_password):
        self.user_id=user_id
        self.user_name=user_name
        self.password=user_password
    def is_valid(name,password):
        sql = "select * from administrator"
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        p=0
        for row in rows:
            if name==row[1] and password==row[2]:
                p = 1
                break
        conn.commit()
        cursor.close()
        conn.close()
        return p
















































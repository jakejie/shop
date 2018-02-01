#-*- coding:utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect, session, flash
from models import *

is_logged = 0
customer = None
app = Flask(__name__)
app.secret_key='666'
#跳转页面7个
@app.route('/')
def index():
    book_list_new = Production.query_by_type_type1("图书","新品上架")
    session.book_list_new = book_list_new
    book_list_social = Production.query_by_type_type1("图书","人文社科")
    session.book_list_social = book_list_social
    book_list_computer = Production.query_by_type_type1("图书","计算机")
    session.book_list_computer = book_list_computer
    book_list_education = Production.query_by_type_type1("图书","教育")
    session.book_list_education = book_list_education
    disk_list = Production.query_by_type("CD")
    session.disk_list = disk_list
    return render_template('index.html')
@app.route('/index2')

def index2():
    book_list_new = Production.query_by_type_type1("图书", "新品上架")
    session.book_list_new = book_list_new
    book_list_social = Production.query_by_type_type1("图书", "人文社科")
    session.book_list_social = book_list_social
    book_list_computer = Production.query_by_type_type1("图书", "计算机")
    session.book_list_computer = book_list_computer
    book_list_education = Production.query_by_type_type1("图书", "教育")
    session.book_list_education = book_list_education
    disk_list = Production.query_by_type("CD")
    session.disk_list = disk_list
    return render_template('index2.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/logged.page')
def logged():
    return render_template('login.html')

@app.route('/customer_registered.page')
def customer_registered():
    return render_template('register.html')

@app.route('/carted.page')
def carted():
    return render_template('cart.html')

@app.route('/cart_finished.page')
def cart_finished():
    return render_template('cart_finish.html')

@app.route('/single_product/product_id=<product_id>')
def single_product(product_id):
    single_product=Production.query_product_by_id(product_id)
    session.single_product=single_product
    return render_template('single-product.html')

@app.route('/customer_manage/user_name=<user_name>')
def customer_manage(user_name):
    user_id = Customer.search_id_by_name(user_name)
    session.customer = Customer.query_all_by_id(user_id)
    session.order=Production.order_production_data(user_id)
    return render_template('customer_manage.html')

@app.route('/seller_manage/seller_name=<seller_name>')
def seller_manage(seller_name):
    seller_id = Seller.search_id_by_name(seller_name)
    session.seller = Seller.query_all_by_id(seller_id)
    session.product_all = Seller.query_seller_product(seller_id)
    return render_template('seller_manage.html')
@app.route('/administrator_manage.page')
def administrator_manage():
    session.customer_all = Customer.query_all()
    session.seller_all = Seller.query_all()
    session.product_all = Production.all_query()
    return render_template('administrator_manage.html')

# 买家登录账户
@app.route('/customer_login',methods=['POST'])
def customer_login():
    form = request.form
    username = form.get('username')
    password = form.get('password')
    if Customer.is_valid(username, password):
        session['username'] = username
        session['password'] = password
        return redirect(url_for('index2'))
    else:
        return "错"
# 卖家登录账户
@app.route('/seller_login', methods=['POST'])
def seller_login():
    form = request.form
    username = form.get('username')
    password = form.get('password')
    if Seller.is_valid(username, password):
        session['username'] = username
        session['password'] = password
        return redirect(url_for('seller_manage',seller_name=username))
    else:
        return "错"

# 管理员登录账户
@app.route('/administrator_login', methods=['POST'])
def administrator_login():
    form = request.form
    username = form.get('username')
    password = form.get('password')
    if Administrator.is_valid(username, password):
        session['username'] = username
        session['password'] = password
        return redirect(url_for('administrator_manage'))
    else:
        return "错"
#注册买家账户
@app.route('/customer_register',methods=['POST'])
def customer_register():
    form = request.form
    username = form.get('username')
    password = form.get('password')
    repassword = form.get('repassword')
    email = form.get('email')
    sex = form.get('sex')
    tel = form.get('phone')
    address = form.get('address')
    check = form.get('check')
    if not username:
        flash("请输入用户名")
        return render_template("register.html")
    if not password:
        flash("请输入密码")
        return  render_template("register.html")
    if not Customer.if_name_is_repeated(username):
        if password == repassword:
            if check == '1':
                session['username'] = username
                session['userid'] = Customer.get_id_by_name(username)
                Customer.save_to_db(username, password, email, sex, tel, address)
                return redirect(url_for('index2'))

            else:
                flash("请阅读网站协议并勾选同意协议框")
                return render_template('register.html')
        else:
            flash("两次输入密码不相同")
            return render_template('register.html')
    else:
        flash("用户名重复")
        return render_template('register.html')

# 注册卖家账户
@app.route('/seller_register', methods=['POST'])
def seller_register():
    form = request.form
    username = form.get('username')
    password = form.get('password')
    repassword = form.get('repassword')
    email = form.get('email')
    sex = form.get('sex')
    full_sub = form.get('full_sub')
    tel = form.get('phone')
    check = form.get('check')
    if not username:
        flash("请输入用户名")
        return render_template("register.html")
    if not password:
        flash("请输入密码")
        return render_template("register.html")
    if not Customer.if_name_is_repeated(username):
        if password == repassword:
            if check == '1':
                session['username'] = username
                session['userid'] = Customer.get_id_by_name(username)
                Seller.save_to_db(username, password, email, sex, tel,full_sub)
                return redirect(url_for('index2'))
            else:
                flash("请阅读网站协议并勾选同意协议框")
                return render_template('register.html')
        else:
            flash("两次输入密码不相同")
            return render_template('register.html')
    else:
        flash("用户名重复")
        return render_template('register.html')


# 买家修改个人信息
@app.route('/customer_change/user_name=<user_name>', methods=['POST'])
def customer_change(user_name):
    user_id = Customer.search_id_by_name(user_name)
    form = request.form
    username = form.get('username')
    password = form.get('password')
    repassword = form.get('repassword')
    email = form.get('email')
    sex = form.get('sex')
    tel = form.get('phone')
    address = form.get('address')
    if not username:
        flash("请输入用户名")
        return render_template("customer_manage.html")
    if not password:
        flash("请输入密码")
        return render_template("customer_manage.html")
    if not Customer.if_name_is_repeated_for_customer_manage(username):
        if password == repassword:
            session['username'] = username
            session['userid'] = Customer.get_id_by_name(username)
            Customer.update_to_db(user_id, username, password, email, sex, tel, address)
            flash("信息更改成功")
            return redirect(url_for('index2'))
        else:
            flash("两次输入密码不相同")
            return render_template('customer_manage.html')
    else:
        flash("用户名重复")
        return render_template('customer_manage.html')

# 卖家修改个人信息
@app.route('/seller_change/user_name=<user_name>', methods=['POST'])
def seller_change(user_name):
    user_id = Seller.search_id_by_name(user_name)
    form = request.form
    username = form.get('username')
    password = form.get('password')
    repassword = form.get('repassword')
    email = form.get('email')
    sex = form.get('sex')
    tel = form.get('phone')
    if not username:
        flash("请输入用户名")
        return render_template("seller_manage.html")
    if not password:
        flash("请输入密码")
        return render_template("seller_manage.html")
    if not Seller.if_name_is_repeated_for_seller_manage(username):
        if password == repassword:
            session['username'] = username
            session['userid'] = Seller.get_id_by_name(username)
            Seller.update_to_db(user_id, username, password, email, sex, tel)
            flash("信息更改成功")
            return redirect(url_for('seller_manage',seller_name=username))
        else:
            flash("两次输入密码不相同")
            return render_template('seller_manage.html')
    else:
        flash("用户名重复")
    return render_template('seller_manage.html')

#卖家添加商品信息
@app.route('/seller_add_product/seller_name=<seller_name>', methods=['POST'])
def seller_add_product(seller_name):
    seller_id = Seller.search_id_by_name(seller_name)
    form = request.form
    add_product_type = form.get('add_product_type')
    add_product_name = form.get('add_product_name')
    add_product_price=form.get('add_product_price')
    add_product_quantity=form.get('add_product_quantity')
    add_product_image=form.get('add_product_image')
    add_product_des = form.get('add_product_des')
    add_product_type1=form.get('add_product_type1')
    add_product_discount = form.get('add_product_discount')
    add_product_full_sub=form.get('add_product_full_sub')
    if add_product_full_sub:
      product_full_sub = Seller.search_fullsub_by_id(seller_id)
    else:
        product_full_sub='0'
    Production.add_new_production(add_product_type,add_product_name,add_product_price,add_product_quantity,add_product_image,add_product_des,add_product_type1)
    print(add_product_name)
    product_id=Production.get_production_id(add_product_name)
    print(product_id)
    Seller.add_new_production(seller_id,product_id,add_product_discount,product_full_sub)
    return redirect(url_for('seller_manage',seller_name=seller_name))
# 卖家删除商品信息
@app.route('/seller_delete_product/product_id=<product_id>,seller_name=<seller_name>')
def seller_delete_product(product_id,seller_name):
    seller_id=Seller.search_id_by_name(seller_name)
    Seller.delete_production(seller_id, product_id)
    return redirect(url_for('seller_manage',seller_name=seller_name))
#卖家修改商品信息
@app.route('/seller_change_product/product_id=<product_id>,seller_name=<seller_name>', methods=['POST'])
def seller_change_product(product_id,seller_name):
    seller_id = Seller.search_id_by_name(seller_name)
    form = request.form
    change_product_type = form.get('change_product_type')
    change_product_name = form.get('change_product_name')
    change_product_price=form.get('change_product_price')
    change_product_quantity=form.get('change_product_quantity')
    change_product_image=form.get('change_product_image')
    change_product_des = form.get('change_product_des')
    change_product_type1=form.get('change_product_type1')
    change_product_discount = form.get('change_product_discount')
    change_product_full_sub = form.get('change_product_full_sub')
    if seller_id == 1:
        if change_product_full_sub!='0':
            product_full_sub = '200-20'
        else:
            product_full_sub = '0'
    elif seller_id == 2:
        if change_product_full_sub!='0':
            product_full_sub = '150-15'
        else:
            product_full_sub = '0'
    Production.edit(product_id,change_product_type,change_product_name,change_product_price,change_product_quantity,change_product_image,change_product_des,change_product_type1)
    Seller.change_production(seller_id, product_id, change_product_discount,product_full_sub)
    return redirect(url_for('seller_manage',seller_name=seller_name))


#添加购物车
@app.route('/add_to_basket', methods=['POST'])
def add_to_basket():
    form = request.form
    user_name = form.get('user_name')
    production_id=form.get('production_id')
    on_sale=Production.get_onsale_by_production_id(production_id)
    if on_sale:
        if (not user_name):
            return redirect(url_for('.logged'))
        else:
            sale=Sale(user_name)
            sale.add_item(production_id)
            session['basket_data'] = Production.basket_production_data(Customer.get_id_by_name(user_name))
            #计算商品总价
            basket_data = session['basket_data']
            session['total']=Sale.get_product_price_total(basket_data)
            session['discount']=Sale.get_price_discount(basket_data)
            session['full_sub']=Sale.get_price_full_sub(basket_data)
            # print(Sale.get_product_price_total(basket_data))
            # print(Sale.get_price_discount(basket_data))
            # print(Sale.get_price_full_sub(basket_data))
            session['real_price']=session['total']-float(session['discount'])-float(session['full_sub'])
            return redirect(url_for('index2'))
    else:
        # print("jjjjjjjjjjjj")
        flash("该商品已下架")
        return redirect(url_for('index2'))
#从index2里面的小购物车里删除
@app.route('/delete_from_basket/order_id=<order_id>,item_id=<item_id>,user_name=<user_name>')
def delete_from_basket(order_id, item_id, user_name):
    Orders.delete_from_basket(order_id, item_id)
    session['basket_data'] = Production.basket_production_data(Customer.get_id_by_name(user_name))
    basket_data = session['basket_data']
    session['total'] = Sale.get_product_price_total(basket_data)
    session['discount'] = Sale.get_price_discount(basket_data)
    session['full_sub'] = Sale.get_price_full_sub(basket_data)
    session['real_price'] = session['total'] - float(session['discount']) - float(session['full_sub'])
    return redirect(url_for('index2'))
#从购物车页面里删除商品  与下面一个函数，只有跳转页面不同
@app.route('/delete_from_basket_when_in_basket/order_id=<order_id>,item_id=<item_id>,user_name=<user_name>')
def delete_from_basket_when_in_basket(order_id,item_id,user_name):
    Orders.delete_from_basket(order_id,item_id)
    session['basket_data'] = Production.basket_production_data(Customer.get_id_by_name(user_name))
    basket_data=session['basket_data']
    session['total']=Sale.get_product_price_total(basket_data)
    session['discount'] = Sale.get_price_discount(basket_data)
    session['full_sub'] = Sale.get_price_full_sub(basket_data)
    session['real_price'] = session['total'] - float(session['discount']) - float(session['full_sub'])
    return redirect(url_for('carted'))
#从购物车页面里增加商品  与下面一个函数，只有跳转页面不同
@app.route('/add_from_basket_when_in_basket/item_id=<item_id>,user_name=<user_name>')
def add_from_basket_when_in_basket(item_id,user_name):
    Orders.add_from_basket(item_id)
    session['basket_data'] = Production.basket_production_data(Customer.get_id_by_name(user_name))
    basket_data=session['basket_data']
    session['total']=Sale.get_product_price_total(basket_data)
    session['discount'] = Sale.get_price_discount(basket_data)
    session['full_sub'] = Sale.get_price_full_sub(basket_data)
    session['real_price'] = session['total'] - float(session['discount']) - float(session['full_sub'])
    return redirect(url_for('carted'))
#结算的从购物车里删除
@app.route('/checkout/user_name=<user_name>')
def checkout(user_name):
    sale = Sale(user_name)
    sale.checkout()
    session['basket_data'] = Production.basket_production_data(Customer.get_id_by_name(user_name))
    return redirect(url_for('cart_finished'))




#管理员添加买家信息
@app.route('/add_customer', methods=['POST'])
def add_customer():
    form = request.form
    add_customer_name = form.get('add_customer_name')
    add_customer_password = form.get('add_customer_password')
    add_customer_email = form.get('add_customer_email')
    add_customer_sex = form.get('add_customer_sex')
    add_customer_tel = form.get('add_customer_tel')
    add_customer_address = form.get('add_customer_address')
    Customer.save_to_db(add_customer_name, add_customer_password,add_customer_email,add_customer_sex,                               add_customer_tel, add_customer_address)
    return redirect(url_for('administrator_manage'))
#管理员删除买家信息
@app.route('/delete_customer/customer_id=<customer_id>')
def delete_customer(customer_id):
    Customer.delete_customer(customer_id)
    return redirect(url_for('administrator_manage'))


#管理员修改买家信息
@app.route('/change_customer/customer_id=<customer_id>', methods=['POST'])
def change_customer(customer_id):
    form = request.form
    change_customer_name = form.get('change_customer_name')
    change_customer_password = form.get('change_customer_password')
    change_customer_email = form.get('change_customer_email')
    change_customer_sex = form.get('change_customer_sex')
    change_customer_tel = form.get('change_customer_tel')
    change_customer_address = form.get('change_customer_address')
    Customer.update_to_db(customer_id,change_customer_name, change_customer_password, change_customer_email,change_customer_sex,
                          change_customer_tel,change_customer_address)
    return redirect(url_for('administrator_manage'))

#管理员添加卖家信息
@app.route('/add_seller', methods=['POST'])
def add_seller():
    form = request.form
    add_seller_name = form.get('add_seller_name')
    add_seller_password = form.get('add_seller_password')
    add_seller_email = form.get('add_seller_email')
    add_seller_sex = form.get('add_seller_sex')
    add_seller_tel = form.get('add_seller_tel')
    Seller.save_to_db(add_seller_name, add_seller_password,add_seller_email,add_seller_sex,add_seller_tel)
    return redirect(url_for('administrator_manage'))
#管理员删除卖家信息
@app.route('/delete_seller/seller_id=<seller_id>')
def delete_seller(seller_id):
    Seller.delete_seller(seller_id)
    return redirect(url_for('administrator_manage'))


#管理员修改卖家信息
@app.route('/change_seller/seller_id=<seller_id>', methods=['POST'])
def change_seller(seller_id):
    form = request.form
    change_seller_name = form.get('change_seller_name')
    change_seller_password = form.get('change_seller_password')
    change_seller_email = form.get('change_seller_email')
    change_seller_sex = form.get('change_seller_sex')
    change_seller_tel = form.get('change_seller_tel')
    Seller.update_to_db(seller_id,change_seller_name, change_seller_password, change_seller_email,change_seller_sex,
                          change_seller_tel)
    return redirect(url_for('administrator_manage'))








#管理员添加商品信息
@app.route('/add_product', methods=['POST'])
def add_product():
    form = request.form
    add_product_type = form.get('add_product_type')
    add_product_name = form.get('add_product_name')
    add_product_price=form.get('add_product_price')
    add_product_quantity=form.get('add_product_quantity')
    add_product_image=form.get('add_product_image')
    add_product_des = form.get('add_product_des')
    add_product_type1=form.get('add_product_type1')
    Production.add_new_production(add_product_type,add_product_name,add_product_price,add_product_quantity,add_product_image,add_product_des,add_product_type1)
    return redirect(url_for('administrator_manage'))
# 管理员修改商品信息
@app.route('/change_product/product_id=<product_id>', methods=['POST'])
def change_product(product_id):
    form = request.form
    change_product_type = form.get('change_product_type')
    change_product_name = form.get('change_product_name')
    change_product_price=form.get('change_product_price')
    change_product_quantity=form.get('change_product_quantity')
    change_product_image=form.get('change_product_image')
    change_product_des = form.get('change_product_des')
    change_product_type1=form.get('change_product_type1')
    Production.edit(product_id,change_product_type,change_product_name,change_product_price,change_product_quantity,change_product_image,change_product_des,change_product_type1)
    return redirect(url_for('administrator_manage'))
# 管理员删除商品信息
@app.route('/delete_product/product_id=<product_id>')
def delete_product(product_id):
    Production.delete_production(product_id)
    return redirect(url_for('administrator_manage'))










# @app.errorhandler(404)
# def error_404(error):
#     """这个handler可以catch住所有abort(404)以及找不到对应router的处理请求"""
#     response = dict(status=0, message="404 Not Found")
#     return jsonify(response), 404


if __name__ == '__main__':
    app.run(debug=True)

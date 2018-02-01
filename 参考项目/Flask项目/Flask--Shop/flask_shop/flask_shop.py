import enum
import math
import os
import re
from datetime import datetime

from PIL import Image

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_required, roles_accepted, current_user, user_registered
from flask_mail import Mail
from flask_babel import Babel, gettext, ngettext, format_datetime
from flask_uploads import UploadSet, IMAGES, configure_uploads
from sqlalchemy import desc
from sqlalchemy.dialects import postgresql
from sqlalchemy.types import CHAR
from jinja2 import Environment, environmentfilter, evalcontextfilter, Markup
from werkzeug.utils import secure_filename

app = Flask(__name__)
#app.config.from_object('flask_shop.default.cfg')
app.config.update(dict(
    # general
    #SERVER_NAME='',
    MAX_CONTENT_LENGTH=512*1024,
    SECRET_KEY='CHANGE_ME fsa$#@%4325#2$used4cookieEnc',
    DEBUG=True,
    # app specific
    TEST_SELLER_MAIL='fake@example.com',
    TEST_SELLER_PASSWORD='CHANGE_ME Password789',
    CURRENCY='PLN',
    PAGE_SIZE=5,
    # flask-sqlalchemy
    SQLALCHEMY_DATABASE_URI='postgresql://shop_writer:CHANGE_ME890@localhost:5432/shop',
    #SQLALCHEMY_TRACK_MODIFICATIONS=True,
    # flask-security
    SECURITY_PASSWORD_HASH='sha512_crypt',
    SECURITY_PASSWORD_SALT='CHANGE_ME ThisIs2ndSalt',
    SECURITY_TOKEN_MAX_AGE=30*60,
    SECURITY_REGISTERABLE=True,
    SECURITY_SEND_REGISTER_EMAIL=True,
    SECURITY_RECOVERABLE=True,
    SECURITY_TRACKABLE=True,
    SECURITY_CHANGEABLE=True,
    # flask-mail
    MAIL_DEBUG = True,
    MAIL_SERVER = 'smtp.example.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'fake@example.com',
    MAIL_PASSWORD = 'CHANGE ME',
    # flask-uploads
    UPLOADED_PHOTOS_DEST='/var/www/flask_shop/uploads'
))
app.config.from_envvar('FLASK_SHOP_CFG', silent=True)

db = SQLAlchemy(app)
babel = Babel(app)
mail = Mail(app)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, (photos))

# REs sanitizing input, wrong chars will be replaces with ''
# All the text in HTML templates is HTML-encoded anyway
RE_TITLE = re.compile('[^\w\s_/\\\'\-\+\(\)]+')
RE_DESC =  re.compile('[^\w\s_/\\\'\-\+\(\)\,\.\?]+')
RE_ADDR =  re.compile('[^\w\s_/\\\'\-\+\(\)\,\.]+')
RE_POSTAL =re.compile('[^\d-]')
RE_PHONE = re.compile('[^\d -]+')

role_user = db.Table('role_user',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))
    
class Address(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    line1 = db.Column(db.String(100), nullable=False)
    line2 = db.Column(db.String(100))
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    postal_code = db.Column(db.String(10))
    country = db.Column(CHAR(2), nullable=False)
    phone = db.Column(db.String(30)) # TODO: better format
    
    def __str__(self):
        ret = self.line1 + '\n'
        if self.line2 != None and self.line2 != '':
            ret += self.line2 + '\n'
        if self.phone != None and self.phone != '':
            ret += self.phone + '\n'
        ret += self.address + '\n'
        ret += self.postal_code + ' ' + self.city + '\n'
        ret += self.country
        return ret

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(postgresql.INET)
    current_login_ip = db.Column(postgresql.INET)
    login_count = db.Column(db.Integer())
    roles = db.relationship('Role', secondary=role_user,
                                    backref=db.backref('users', lazy='dynamic'))
    address = db.relationship('Address', backref='user', lazy='dynamic')

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    seller_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(255))
    pic = db.Column(db.String(100), unique=True)
    price = db.Column(db.Float(), nullable=False) # no postgresql.MONEY type...
    visible = db.Column(db.Boolean(), default=True, nullable=False)

class BoughtProduct(db.Model):
    id = db.Column(db.Integer(), primary_key=True)    
    product_id = db.Column(db.Integer(), db.ForeignKey('product.id'))
    product = db.relationship('Product')
    quantity = db.Column(db.Integer(), nullable=False)
    order_id = db.Column(db.Integer(), db.ForeignKey('order.id'))

    def price(self):
        return self.quantity * self.product.price

ORDER_STATE_NAMES = [
    gettext('In progress'),
    gettext('Payment not yet confirmed'),
    gettext('Payment invalid'),
    gettext('Payment confirmed'),
    gettext('Product was sent')
]
class OrderState(enum.IntEnum):
    Unfinished = 0,
    PaymentUnconfirmed = 1,
    PaymentInvalid = 2,
    PaymentConfirmed = 3,
    ProductSent = 4
    
    def __str__(self):
        return ORDER_STATE_NAMES[self.value]

# order is per-seller
class Order(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    seller = db.relationship('User', foreign_keys = seller_id)
    buyer_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    buyer = db.relationship('User', foreign_keys = buyer_id)
    created = db.Column(db.DateTime(), nullable=False)
    modified = db.Column(db.DateTime(), nullable=False)
    address_id = db.Column(db.Integer(), db.ForeignKey('address.id'))
    address = db.relationship('Address')
    state = db.Column(db.Enum(OrderState), nullable=False, default=OrderState.Unfinished)
    bought = db.relationship('BoughtProduct', backref='order', lazy='dynamic')
    
    def total(self):
        ret = 0.00
        for prod in self.bought:
            ret += prod.price()
        return ret

# This should NOT be saved to DB
class CreditCardPayment:
    def __init__(self, order_id, provider, number, cv2, expires):
        self.order_id = order_id
        self.provider = provider
        self.number = number
        self.cv2 = cv2
        self.expires = expires

@app.template_filter()
def format_currency(value):
    return  '{0:20,.2f} {1}'.format(value, app.config['CURRENCY'])

app.add_template_filter(format_datetime)

@app.template_filter()
@evalcontextfilter
def nl2br(ctx, text):
    text = text.replace('\n', '<br>')
    if ctx.autoescape:
        return Markup(text)
    return text

@babel.localeselector
def get_locale():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    return request.accept_languages.best_match(['en', 'pl'])

@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

@app.errorhandler(413)
def error413(e):
    return 'Request too large, max size is %d KB' % (app.config['MAX_CONTENT_LENGTH']/1024), 413

@app.cli.command('initdb')
def init_db():
    db.reflect()
    db.drop_all()
    db.create_all()
    user_datastore.find_or_create_role(name = 'seller', description = 'Person who can add products')
    user_datastore.find_or_create_role(name = 'buyer', description = 'Person who can buy products')
    if not user_datastore.get_user(app.config['TEST_SELLER_MAIL']):
        user_datastore.create_user(email = app.config['TEST_SELLER_MAIL'],
                                   password = app.config['TEST_SELLER_PASSWORD'],
                                   roles = ['seller', 'buyer'])
    db.session.commit()

@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
    default_role = user_datastore.find_role('buyer')
    user_datastore.add_role_to_user(user, default_role)
    db.session.commit()

@app.route('/')
@login_required
def search():
    page_size = app.config['PAGE_SIZE']
    page = request.args.get('page', 1)
    page = int(page)
    products = Product.query.filter_by(visible = True) \
                            .order_by(desc(Product.id)) \
                            .paginate(page, page_size, False)
    return render_template('search.html',
                            products=products.items,
                            page=page,
                            max_page=math.ceil(products.total/page_size))

@app.route('/product/sell', methods=['GET', 'POST'])
@roles_required('seller')
def sell():
    if request.method == 'GET':
        return render_template('sell.html', currency=app.config['CURRENCY'])

    # Required fields
    if request.form['name'] == None \
    or request.files['img'] == None \
    or request.form['price'] == None:
        abort(400, 'Required fields are missing')
        return

    product = Product()
    product.seller_id = current_user.id
    product.name = RE_TITLE.sub('', request.form['name'])
    product.desc = RE_DESC.sub('', request.form.get('desc', ''))
    
    # pic & thumbnail
    img_file = request.files['img']
    product.pic = photos.save(img_file)
    img = Image.open(img_file)
    img.thumbnail((100, 100), Image.ANTIALIAS)
    img.save(app.config['UPLOADED_PHOTOS_DEST']+'/tn_'+product.pic, img.format)
    
    product.price = float(request.form['price'])
    db.session.add(product)
    db.session.commit()
    flash(gettext('Product was put on sale'), 'success')
    
    return redirect(url_for('search'))

@app.route('/product/buy', methods=['POST'])
@roles_required('buyer')
def buy():
    product = BoughtProduct()
    product.product_id = int(request.form['product_id'])
    if Product.query.get(product.product_id) == None:
        abort(404, 'No such product')
        return
    
    product.quantity = int(request.form.get('quantity', '1'))
    db.session.add(product)
    db.session.commit()
    
    order = Order.query.filter_by(buyer_id = current_user.id,
                                  seller_id = product.product.seller_id,
                                  state = OrderState.Unfinished).first()
    # create a new order if none for this seller yet
    if order == None:
        order = Order()
        order.buyer_id = current_user.id
        order.seller_id = product.product.seller_id
        order.state = OrderState.Unfinished
        order.created = order.modified = datetime.utcnow()
        db.session.add(order)
        db.session.commit()
        db.session.flush()
    
    product.order_id = order.id
    db.session.commit()    
    flash(gettext('Product was added to your order'), 'success')
    
    return redirect(url_for('search'))

@app.route('/product/remove/<id>')
@roles_required('seller')
def product_remove_from_sale(id):
    product = Product.query.get(int(id))
    if product == None or product.seller_id != current_user.id:
        abort(401, 'Wrong product')
        return
    
    # We cannot remove the product completely as it can be referenced in buyer orders
    product.visible = False
    db.session.commit()
    flash(gettext('Product is no longer sale'), 'info')
    
    return redirect(url_for('search'))

@app.route('/product/pics/<filename>')
@login_required
def product_picture(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/product/<id>')
@roles_required('buyer')
def product(id):
    return render_template('product.html', product=Product.query.get(int(id)))

@app.route('/order/<id>')
@roles_accepted('buyer', 'seller')
def order(id):
    order = Order.query.get(int(id))
    if order.buyer_id != current_user.id and order.seller_id != current_user.id:
        abort(401, 'This is not your order')
        return
    return render_template('order.html', order=order,
                                         is_buyer=(order.buyer_id == current_user.id))

@app.route('/orders_buyer')
@roles_required('buyer')
def orders_buyer():
    return render_template('orders.html', 
                            orders=Order.query.filter_by(buyer_id = current_user.id).order_by(Order.modified),
                            state_enum=OrderState,
                            is_buyer=True)

@app.route('/orders_seller')
@roles_required('seller')
def orders_seller():
    return render_template('orders.html', 
                            orders=Order.query.filter_by(seller_id = current_user.id).order_by(Order.modified),
                            state_enum=OrderState,
                            is_buyer=False)

@app.route('/order/pay', methods=['GET', 'POST'])
@roles_required('buyer')
def pay():
    order = None
    if request.method == 'GET':
        order = Order.query.get(int(request.args.get('order_id')))
    else:
        order = Order.query.get(int(request.form.get('order_id')))
    
    if order == None \
    or order.buyer_id != current_user.id \
    or order.state != OrderState.Unfinished:
        abort(401, 'Wrong order')
        return

    if request.method == 'GET':
        return render_template('pay.html', order=order)
    
    # required address fields
    if request.form['line1'] == None \
    or request.form['address'] == None \
    or request.form['city'] == None \
    or request.form['country'] == None:
        abort(400, 'Required fields are missing')
        return
    
    address = Address()
    address.user_id = current_user.id
    address.line1 = RE_ADDR.sub('', request.form['line1'])
    address.line2 = RE_ADDR.sub('', request.form.get('line2', ''))
    address.address = RE_ADDR.sub('', request.form['address'])
    address.city = RE_ADDR.sub('', request.form['city'])
    address.postal_code = RE_POSTAL.sub('', request.form.get('postal_code', ''))
    address.country = RE_ADDR.sub('', request.form['country'])
    address.phone = RE_PHONE.sub('', request.form.get('phone', ''))
    db.session.add(address)
    db.session.commit()
    db.session.flush()
    
    #payment = CreditCardPayment(
        #order_id = order.id,
        #provider = None, #request.form['card_provider'],
        #number = request.form['card_number'],
        #cv2 = request.form['card_cv2'],
        #expires = None)

    order.address_id = address.id
    order.state = OrderState.PaymentUnconfirmed
    order.modified = datetime.utcnow()
    db.session.commit()
    flash(gettext('Order was made'), 'success')
    
    return redirect(url_for('orders_buyer'))

@app.route('/order/remove/<order_id>/<bought_product_id>')    
@roles_required('buyer')
def remove(order_id, bought_product_id):
    order = Order.query.get(int(order_id))
    if order == None or order.buyer_id != current_user.id or order.state != Order.Unfinished:
        abort(401, 'Wrong order')
        return
    
    product = BoughtProduct.query.get(int(bought_product_id))
    if product == None or product.order_id != order.id:
        abort(401, 'Wrong product')
        return
        
    db.session.delete(product)
    db.session.commit()
    flash(gettext('Product was removed from the order'), 'info')
    
    return redirect(url_for('orders_buyer'))

@app.route('/order/<order_id>/change_state', methods=['POST'])
@roles_required('seller')
def change_state(order_id):
    order = Order.query.get(int(order_id))
    if order == None or order.seller_id != current_user.id:
        abort(401, 'Wrong order')
        return
    
    order.state = OrderState(int(request.form['new_state']))
    order.modified = datetime.utcnow()
    db.session.commit()
    
    return redirect(url_for('orders_seller'))

if __name__ == '__main__':
    app.run()

from shopApp import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Category(db.Model):
	'''docstring'''
	id = db.Column(db.Integer, primary_key=True)
	categoryName = db.Column(db.String(64), index=True, unique=True)
	description = db.Column(db.String(500))
	products = db.relationship('Product', backref='items', lazy='dynamic')
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


	def __repr__(self):
		return '<Category {}>'.format(self.categoryName)

class Product(db.Model):
	'''docstring'''
	id = db.Column(db.Integer, primary_key=True)
	product_name = db.Column(db.String(64), index=True, unique=True)
	product_description = db.Column(db.String(500))
	price = db.Column(db.String(10))
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Product{}>'.format(self.product_name)


class User(UserMixin, db.Model):
	"""docstring for User"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(60), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	products = db.relationship('Product', backref='products_bought', lazy='dynamic')
	categories = db.relationship('Category', backref='categories_created', lazy='dynamic')
	picture = db.Column(db.String(500))

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User{}>'.format(self.username)

# User Loader Function
# keeps track of the logged in user by storing its unique identifier in Flask's user session
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
		
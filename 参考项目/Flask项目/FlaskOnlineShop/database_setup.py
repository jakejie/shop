from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):
	''' 
	docstring
	'''
	__tablename__ = 'category'

	id = Column(Integer,primary_key=True)
	name = Column(String(100), nullable=False)
	description = Column(String(300), nullable=False)


	def __init__(self, name, description):

		self.name = name
		self.description = description

	def __repr__(self):
		return '<id: {}>'.format(self.id)


	def __str__(self):
		return 'name: {}'.format(self.name)



class Product(Base):

	'''
		Docstring
	'''

	__tablename__ = 'product'

	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable= False)
	description = Column(String(250), nullable=False)
	price = Column(String(50), nullable=False)
	category_id = Column(Integer, ForeignKey('category.id'))

	category = relationship(Category)


	def __init__ (self, name, description, price, category):
		self.name = name
		self.description = description
		self.price = price
		self.category = category

		


	def __repr__(self):
		return '<id: {}>'.format(self.id)


	def __str__(self):
	 	return '<name: {}>'.format(self.name)




class User(Base):
	''' docstring '''

	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	password = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	picture = Column(String(250), nullable=True)


	def __init__(self, name, email, picture):
		self.name = name
		self.email = email
		self.picture = picture


	def __repr__(self):
		return '<id {}>'.format(self.id)

	def __str__(self):
		return '<name {}>'.format(self.name)




class Cart(Base):
	''' docstring '''

	__tablename__ = 'cart'

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'))
	product_id = Column(Integer, ForeignKey('product.id'))
	category_id = Column(Integer, ForeignKey('category.id'))

	user = relationship(User)
	product = relationship(Product)
	category = relationship(Category)


	def __init__(self):
		items = []

	def __repr__(self):
		return '<id {}>'.format(self.id)



engine = create_engine('sqlite:///trialDatabaseUsersCart.db')
Base.metadata.create_all(engine)

print("Database created")
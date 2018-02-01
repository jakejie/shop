from flask import render_template, redirect, url_for, request

# Imports required for sqlalchemy
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Product, User, Cart


# Connect to Database and create database session
engine = create_engine('sqlite:///trialDatabaseUsersCart.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

from . import admin


@admin.route("/categories/")
def allCategories():
	return render_template('allCategories.html')

@admin.route("/categories/<string:category_name>/<int:id>/")
def specificCategory(category_name,id):
	category = session.query(Category).filter_by(id=id, name=category_name).one()
	products = session.query(Product).filter_by(category_id=category.id)

	return render_template('specificCategory.html', category=category, products=products)

@admin.route("/categories/add/", methods=['GET','POST'])
def addCategory():
	if request.method == 'POST':
		if request.form['name'] and request.form['description']:
			newCategory = Category(name=request.form['name'], description=request.form['description'])
			session.add(newCategory)
			session.commit()
			return redirect(url_for('homepage'))
		else:
			return redirect(url_for('pageNotFound'))

	else:
		return render_template("addCategory.html")

@admin.route("/categories/<int:id>/edit/", methods=['GET', 'POST'])
def editCategory(id):
	editCategory = session.query(Category).filter_by(id=id).one_or_none()
	if editCategory:
		if request.method == 'POST':
			if request.form['name'] and request.form['description']:
				editCategory.name = request.form['name']
				editCategory.description = request.form['description']
				session.add(editCategory)
				session.commit()
				return redirect(url_for('homepage'))
			else:
				return render_template('ErrorPage.html')
		else:
			return render_template('editCategory.html', category=editCategory)
	else:
		return redirect(url_for('pageNotFound'))


@admin.route("/categories/<int:id>/delete/", methods=['GET', 'POST'])
def deleteCategory(id):
	deleteCategory = session.query(Category).filter_by(id=id).one_or_none()
	if deleteCategory:
		if request.method == 'POST':
			session.delete(deleteCategory)
			session.commit()
			return redirect(url_for('homepage'))
		else:
			return render_template('deleteCategory.html', category=deleteCategory)
	else:
		return redirect(url_for('pageNotFound'))


@admin.route("/products/<int:category_id>/<string:product_name>/<int:product_id>/")
def products(category_id, product_name, product_id):
	category = session.query(Category).filter_by(id=category_id).one_or_none()
	products = session.query(Product).filter_by(name=product_name, id=product_id).all()
	return render_template('products.html', category=category, products=products)


@admin.route("/products/add/", methods=['GET','POST'])
def addProduct():
	categories = session.query(Category).order_by(asc(Category.name))

	if request.method == 'POST':
		if request.form.get('category'):
			category_id = request.form.get('category')
			category = session.query(Category).filter_by(id=category_id).one_or_none()
		if request.form['name']:
			newProduct = Product(name=request.form['name'], price=request.form['price'], description=request.form['description'], category=category)
			session.add(newProduct)
			session.commit()
			print("done")
			return redirect(url_for('specificCategory', id=category_id, category_name=category.name))
		else:
			return redirect(url_for('pageNotFound'))
	else:
		return render_template('addProduct.html', categories=categories)


# route todo well
@admin.route("/products/<string:category_name>/<int:product_id>/edit/", methods=['GET','POST'])
def editProduct(category_name, product_id):
	categories = session.query(Category).order_by(asc(Category.name))
	editProduct = session.query(Product).filter_by(id=product_id).one_or_none()
	if editProduct:
		if request.method == 'POST':
			if request.form.get('category'):
				category_id = request.form.get('category')
				category = session.query(Category).filter_by(id=category_id).one_or_none()
				editProduct.category = category
			if request.form['name']:
				editProduct.name = request.form['name']
			if request.form['price']:
				editProduct.price=request.form['price']
			if request.form['description']:
				description=request.form['description']

			session.add(editProduct)
			session.commit()
			return redirect(url_for('specificCategory', id=category_id, category_name=category.name))
		else:
			return render_template('editProduct.html', categories=categories, product=editProduct)
	else:
		return redirect(url_for('pageNotFound'))

#app.route to do well
@admin.route("/products/<int:id>/<int:product_id>/delete/", methods=['GET', 'POST'])
def deleteProduct(id, product_id):
	deleteProduct = session.query(Product).filter_by(id=product_id).one_or_none()
	category = session.query(Category).filter_by(id=id).one_or_none()
	if deleteProduct:
		if request.method == 'POST':
			session.delete(deleteProduct)
			session.commit()
			return redirect(url_for('specificCategory', id=id, category_name=category.name))
		else:
			return render_template('deleteProduct.html', product=deleteProduct)
	else:
		return redirect(url_for('pageNotFound'))

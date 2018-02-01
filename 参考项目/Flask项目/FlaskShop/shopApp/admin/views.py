from flask import render_template, redirect, url_for, request
from shopApp.admin import admin
from shopApp import db
from shopApp.models import Category, Product, User
from shopApp.admin.forms import CategoryForm, ProductForm



@admin.route('/')
def adminHomepage():
	categories = db.session.query(Category)
	products =db.session.query(Product)
	return render_template('admin/adminHomepage.html', categories=categories, products=products)


@admin.route('/categories/')
def allCategories():
	return render_template('admin/allCategories.html')

@admin.route('/specificCategory/')
def specificCategory():
	return render_template('admin/specificCategory.html')

@admin.route('/addCategory/', methods=['GET','POST'])
def addCategory():
	form = CategoryForm()
	if form.validate_on_submit():
		category = Category(categoryName=form.categoryName.data, description=form.description.data)
		db.session.add(category)
		db.session.commit()
		return redirect(url_for('admin.adminHomepage'))
	return render_template('admin/addCategory.html', form=form)

@admin.route('/editCategory/<int:id>/', methods=['GET','POST'])
def editCategory(id):
	category = db.session.query(Category).filter_by(id=id).first()
	if category:
		form = CategoryForm()
		if form.validate_on_submit():
			category.categoryName = form.categoryName.data
			category.description = form.description.data
			db.session.add(category)
			db.session.commit()
			return redirect(url_for('admin.adminHomepage'))
	return render_template('admin/editCategory.html', form=form, category=category)

@admin.route('/deleteCategory/<int:id>/', methods=['GET', 'POST'])
def deleteCategory(id):
	category = db.session.query(Category).filter_by(id=id).first()
	if category and request.method == 'POST':
		db.session.delete(category)
		db.session.commit()
		return redirect(url_for('admin.adminHomepage'))
	return render_template('admin/deleteCategory.html')

@admin.route('/addProduct/', methods=['GET','POST'])
def addProduct():
	form = ProductForm()
	form.category_id.choices = [(g.id, g.categoryName) for g in Category.query.order_by('categoryName')]
	if form.validate_on_submit():
		product= Product(product_name=form.product_name.data, product_description=form.product_description.data, price=form.price.data, category_id=form.category_id.data)
		db.session.add(product)
		db.session.commit()
		return redirect(url_for('admin.adminHomepage'))
	return render_template('admin/addProduct.html', form=form)

@admin.route('/editProduct/<string:categoryName>/<int:product_id>/', methods=['GET', 'POST'])
def editProduct(categoryName,product_id):
	product=db.session.query(Product).filter_by(id=product_id).first()
	if product:
		form = ProductForm()
		form.category_id.choices = [(g.id, g.categoryName) for g in Category.query.order_by('categoryName')]
		if form.validate_on_submit():
			product.product_name=form.product_name.data
			product.product_description=form.product_description.data
			product.price =form.price.data
			product.category_id=form.category_id.data
			db.session.add(product)
			db.session.commit()
			return redirect(url_for('admin.adminHomepage'))
	else:
		return 'opps'
	return render_template('admin/editProduct.html', form=form)

@admin.route('/deleteProduct/')
def deleteProduct():
	return render_template('admin/deleteProduct.html')
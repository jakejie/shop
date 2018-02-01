from flask import render_template, redirect, url_for
from . import home

# Imports required for sqlalchemy
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Product, User, Cart


# Connect to Database and create database session
engine = create_engine('sqlite:///trialDatabaseUsersCart.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#flask wtf
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap



class MyForm(Form):
    name = StringField('name', validators=[DataRequired()])


@home.route("/")
def homepage():
	categories = session.query(Category).order_by(asc(Category.name))
	products = session.query(Product).order_by(asc(Product.name))
	return render_template('homepage.html', products=products, categories=categories)


@home.route("/login/", methods=['GET', 'POST'])
def login():
	return render_template('login.html')

@home.route("/register/")
def register():
	form = MyForm()
	return render_template('register.html', form=form)
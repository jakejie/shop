from flask import Flask, render_template, request, redirect, url_for
from flask import Blueprint
app = Flask(__name__)



# Imports required for sqlalchemy
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Product, User, Cart


# Connect to Database and create database session
def connectDB():
	engine = create_engine('sqlite:///trialDatabaseUsersCart.db')
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind=engine)
	session = DBSession()

from flask_bootstrap import Bootstrap
Bootstrap(app)
#Blueprint imports
from admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')


from home import home as home_blueprint
app.register_blueprint(home_blueprint)

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')


@app.route("/pageNotFound/")
def pageNotFound():
	return render_template('ErrorPage.html')

@app.route("/categories/")
def allCategories():
	return render_template('allCategories.html')


@app.route("/user/<int:user_id>/<string:user_name>/")
def userProfile(user_id,user_name):
	return render_template('userProfile.html')

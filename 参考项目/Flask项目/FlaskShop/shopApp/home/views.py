from flask import render_template, redirect, url_for
from shopApp.home import home
from shopApp import db
from shopApp.home.forms import LoginForm, RegistrationForm
from shopApp.models import User
from flask_login import current_user, login_user, login_required, logout_user


@home.route('/')
@home.route('/home/')
def homepage():
    return render_template('home/homepage.html')

@home.route('/register/', methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('home.login'))
	return render_template('register.html', form=form)

@home.route('/login/', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.userProfile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('home.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home.userProfile'))
    return render_template('login.html', form=form)


@home.route('/userProfile/')
@login_required
def userProfile():
	return render_template('userProfile.html')

@home.route('/logout/')
def logout():
	logout_user()
	return redirect(url_for('home.homepage'))

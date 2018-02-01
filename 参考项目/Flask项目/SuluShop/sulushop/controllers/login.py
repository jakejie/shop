#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from sulushop import app
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import make_response
from flask import flash
from flask import session
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import *

from ..models import *
from ..views import *
from ..util import *
from registro import RegistroForm

#formulario para login
class LoginForm(Form):
    email = StringField('email', validators=[NumberRange(min=4)])
    password = PasswordField('password')
#login get
@app.route('/login/', methods=['GET'])
@logout_required
def regLog():
    '''
    Router: solo accesible mediante el método GET de HTTP/HTTPS.

    Descripción: regLog devuelve una template de registro_login.htmlself.
    Pasa como datos una estructura para almacenar los datos de usuario, un formulario de login,
    y un formulario de registro.

    Función: envia a la ruta de registro_login.html
    '''
    formulario = LoginForm()
    regform = RegistroForm()
    data = get_user_cookie()
    return render_template("_views/registro_login.html", saves=data, loginForm = formulario, registroForm =regform)
#login post
@app.route('/login/', methods=['POST'])
@logout_required
def login():
    '''
    Router: solo accesible mediante el método POST de HTTP/HTTPS.

    Descripción: login redirecciona al router de index si el proceso de login es
    correcto, o al router de login de lo contrarioself.

    Función: recupera el formulario de login y procede a la validación de sus datos.
    '''
    formulario = LoginForm(request.form)
    e_mail = formulario.data['email']
    clave = get_user_contrasena(e_mail)
    data = get_user_cookie()
    if formulario.validate() and clave == formulario.data['password']:
        session['email'] = e_mail
        session['username'] = formulario.data['email']
        data.update(formulario.data)
        response = make_response(redirect(url_for('index')))
        response.set_cookie('character', json.dumps(data))
        flash('Login Completado', 'success')
    else :
        flash('Datos Incorrectos', 'danger')
        response = make_response(redirect(url_for('login')))
    return response
#logout del usuario
@app.route('/logout/', methods=['GET'])
@login_required
def loggout():
    '''
    Router: solo accesible mediante el método GET de HTTP/HTTPS.

    Descripción: loggout redirecciona al router de index.

    Función: elimina los cookies y la session de usario, para completar
    el proceso de logout.
    '''

    response = make_response(redirect(url_for('index')))
    data = {}
    if 'username' in session:
        session.pop('username')
    if 'email' in session:
        session.pop('email')
    response.set_cookie('character', json.dumps(data))
    flash('Logout Completado', 'success')
    return response

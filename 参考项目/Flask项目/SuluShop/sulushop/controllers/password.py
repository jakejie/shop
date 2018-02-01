#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from sulushop import app
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import make_response
from flask import flash

from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import *


from ..models import *
from ..views import *
from ..util import *

class CambioForm(Form):
	oldPassword = PasswordField('oldpassword')
	newPassword = PasswordField('newpassword')
	repeatPassword = PasswordField('repeatpassword')


@app.route('/changePassword/', methods=['GET'])
@login_required
def cambiarpassw():
	'''
	Router: solo accesible mediante el método GET de HTTP/HTTPS

	Descripcion: cambiopassw() envia a password.html
	Funcion: devuelve render_template("_modules/password.html")
	'''
	formulario = CambioForm()
	data = get_user_cookie()
	return render_template("_modules/password.html", saves=data, cambioForm = formulario)

@app.route('/changePassword/', methods=['POST'])
@login_required
def cambiopassw():
	'''
	Router: solo accesible mediante el método POST de HTTP/HTTPS

	Descripcion: cambiopasw() toma los datos del formulario cambioForm y los analiza. oldPassword es la contrasena del usuario
			antigua que quiere cambiar, si no coincide con la almacenada en la base de datos, aparece un mensaje de
			error. newPassword y repeatPassword son la nueva contrasena deseada, si no coinciden, aparece un mensaje
			de error. Si todo es correcto,la antigua contrasena sustituye a la nueva contrasena en la base de datos
	Funcion: Cambia la contrasena del usuario
	'''
	formulario = CambioForm(request.form)
	usuario = get_user()
	if formulario.data['newPassword'] == formulario.data['repeatPassword'] :
		if formulario.data['oldPassword'] == usuario.contrasena:
			flash('Cambio de password exitoso', 'success')
			db.session.delete(usuario)
			usuario.contrasena = formulario.data['newPassword']
			db.session.add(usuario)
			db.session.commit()
			return make_response(redirect(url_for('perfil')))
		else :
			flash('Contrasena incorrecta', 'danger')
			return make_response(redirect(url_for('cambiopassw')))
	else :
		flash('Las contrasenas no coinciden', 'danger')
		return make_response(redirect(url_for('cambiopassw')))

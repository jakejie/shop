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
#formulario de registro
class RegistroForm(Form):
	email = StringField('email', validators=[NumberRange(min=4)])
	password = PasswordField('password')
	nombre = StringField('nombre')
	apellidos = StringField('apellidos')
	nacimiento = StringField('nacimiento')
	direccion = StringField('direccion')
	telefono = StringField('telefono')

#inserta un nuevo usario a la base de Datos
#requiere un parametro cookie('character')
def insert_usuario(data):
	'''
    Descripción: insert_usuario requiere parametro data con
	la información de registro. Este tipo de estructura se obtiene de get_user_cookie().

    Función: inserta un nuevo usuario a la base de datos.
    '''
	usuario = Usuario()
	usuario.nombre = data.get('nombre', ' ')
	usuario.apellidos = data.get('apellidos', ' ')
	usuario.fecha_nacimiento = data.get('nacimiento', ' ')
	usuario.direccion = data.get('direccion', ' ')
	usuario.email = data.get('email', ' ')
	usuario.telefono = data.get('telefono', ' ')
	usuario.contrasena = data.get('password', ' ')
	usuario.imagen = '/static/img/avatar.jpg'
	db.session.add(usuario)
	db.session.commit()

#registro post, obtiene datos de registro
@app.route('/registro', methods=['POST'])
@logout_required
def registro():
	'''
    Router: solo accesible mediante el método POST de HTTP/HTTPS.

    Descripción: registro redirecciona al router de perfil.

    Función: recupera el formulario de registro, pasa los datos a insert_usuario
	,y crea una cookie y una session para el usuario.
    '''
	formulario = RegistroForm(request.form)
	response = make_response( redirect(url_for('perfil')))
	data = get_user_cookie()
	data.update(formulario.data)
	session['email'] = formulario.data['email']
	session['username'] = formulario.data['nombre']
	insert_usuario(data)
	response.set_cookie('character', json.dumps(data))
	flash('Registro Completado', 'success')
	return response

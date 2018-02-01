#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sulushop import app
from flask import request
from flask import render_template
from flask import flash

from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import *

from ..models import *
from ..views import *
from ..util import *

from favorito import UpdateList
from registro import RegistroForm
#formulario para modificar imagen de perfil
class ImgPerfilForm(Form):
    imagen = StringField('imagen')



#elimina la cuenta del usuario actual
@app.route('/deletUser/', methods=['GET'])
@login_required
def deletUser():
    '''
    Router: accesible mediante el método GET de HTTP/HTTPS.

    Descripción: deletUser redirecciona al router de index.

    Función: Elimina todos los datos almacenados en la base de datos referentes
    al usario y hace logout.
    '''
    response = make_response(redirect(url_for('index')))
    data = get_user_cookie()
    usuario = get_user()
    db.session.delete(usuario)
    db.session.commit()

    data = {}
    if 'username' in session:
        session.pop('username')
    if 'email' in session:
        session.pop('email')
    response.set_cookie('character', json.dumps(data))
    return response

#perfil get, devuelve la informacion del perfil
@app.route('/perfil/', methods=['GET'])
@login_required
def perfil():
    '''
    Router: solo accesible mediante el método GET de HTTP/HTTPS.

    Descripción: perfil devuelve una template de perfil.html. Pasa los datos
    del usuario obtenidos mediante get_user y el formulario para cambiar la imagen,
    de perfil.

    Función: envia a la ruta de perfil.html con todos los datos referentes al usuario.
    '''
    data = get_user_cookie()
    usuario = get_user()
    action=get_action_list()
    favorites=get_favorite_list()
    form = UpdateList()
    imgForm = ImgPerfilForm()
    return render_template("_views/perfil.html", user=usuario, logueado=data,
            action=action, favorites=favorites, form=form, imgForm=imgForm)

#modificar la imagen de perfil del usuario mediante url
@app.route('/mod_img/', methods=['POST'])
@login_required
def mod_img():
    '''
    Router: solo accesible mediante el método POST de HTTP/HTTPS.

    Descripción: mod_img devuelve una llamada a perfil para que actualice la template con los
    los cambios de información referentes a la nueva imagen de perfil.

    Función: recupera la información del formulario de cambio de imagen de perfil y actualiza
    la inforamción de la base de datos.
    '''
    formulario = ImgPerfilForm(request.form)
    usuario = get_user()
    db.session.delete(usuario)
    usuario.imagen = formulario.data['imagen']
    db.session.add(usuario)
    db.session.commit()
    flash('Imagen de perfil cambiada', 'success')
    return perfil()

#modificar datos de usuario [get, post]
#permite modificar los datos almacenados referentes al usuario
@app.route('/mod_datos/', methods=['GET', 'POST'])
@login_required
def mod_datos():
    '''
    Router: accesible mediante los métodos GET y POST de HTTP/HTTPS.

    Descripción: para el GET devuelve la template del modificar.html con un formulario para
    modificar los datos de usuario, para el POST recupera la información del formulario y
    la inserta en la base de datos luego redirecciona a perfil .

    Función: se encarga de la modificación de los datos del usuario
    '''
    if request.method == 'GET' :
        formulario = RegistroForm()
        usuario = get_user()
        data = get_user_cookie()
        return render_template("_modules/modificar.html", saves=data, user=usuario, registroForm = formulario)
    else :
        formulario = RegistroForm(request.form)
        data = get_user_cookie()
    	data.update(formulario.data)
        usuario = get_user()
        db.session.delete(usuario)
    	usuario.nombre = data.get('nombre', ' ')
    	usuario.apellidos = data.get('apellidos', ' ')
    	usuario.fecha_nacimiento = data.get('nacimiento', ' ')
    	usuario.direccion = data.get('direccion', ' ')
    	usuario.email = data.get('email', ' ')
    	usuario.telefono = data.get('telefono', ' ')
        db.session.add(usuario)
        db.session.commit()
        imgForm = ImgPerfilForm()
        action=get_action_list()
        favorites=get_favorite_list()
        form = UpdateList()
        flash('Datos Modificados Satisfactoriamente', 'success')
        return render_template("_views/perfil.html", user=usuario, logueado=data,
                action=action, favorites=favorites, form=form, imgForm=imgForm)

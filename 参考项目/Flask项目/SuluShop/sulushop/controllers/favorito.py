#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from sulushop import app
from flask import request
from flask import make_response
from flask import redirect
from flask import url_for
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField
from wtforms.validators import NumberRange, DataRequired


from ..models import *
from ..util import *
from ..decorators import *


class UpdateList(FlaskForm):
    '''
    Parámetros: hereda de la clase FlaskForm

    Descripción: UpdateList realiza las validaciones pertinentes contenidas en
    cada atributo de validators.
    '''
    pk = IntegerField('pk', validators=[NumberRange(min=0)])
    name = StringField('name', validators=[DataRequired()])


@app.route('/lista/add/', methods=['POST'])
@login_required
def add_to_list():
    '''
    Router: solo accesible mediante el método POST de HTTP/HTTPS.

    Descripción: add_to_list redirecciona al router de la función details.
    Toma como datos el nombre y la clave primaria del formulario UpdateList.

    Función: añade un producto a lista con el atributo accion = favorito
    '''
    form = UpdateList(request.form)
    pk = form.data['pk']
    name = form.data['name']

    if form.validate_on_submit():
        product = Lista()
        product.accion = 'favorito'
        product.fecha = datetime.datetime.utcnow()
        product.id_usuario = get_user_id()
        product.id_producto = pk

        db.session.add(product)
        flash('Has añadido {} a favoritos'.format(name), 'success')

    db.session.commit()

    return make_response(redirect(url_for('details', name=name, pk=pk)))


@app.route('/lista/delete/', methods=['POST'])
@login_required
def delete_from_list():
    '''
    Router: solo accesible mediante el método POST de HTTP/HTTPS.

    Descripción: delete_from_list redirecciona al router de la función perfil.
    Toma como datos el nombre y la clave primaria del formulario UpdateList.

    Función: elimina un producto a lista con el atributo accion = favorito
    '''
    form = UpdateList(request.form)
    pk = form.data['pk']
    name = form.data['name']

    if form.validate_on_submit():
        products = Lista.query.filter_by(
            id_usuario = get_user_id(),
            id_producto = pk,
            accion = 'favorito',
            ).all()

        for favorite in products:
            db.session.delete(favorite)
            flash('Has eliminado {} de favoritos'.format(name), 'warning')

        db.session.commit()

    return make_response(redirect(url_for('perfil')))

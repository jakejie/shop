#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from sulushop import app
from flask import request
from flask import render_template
from flask import make_response
from flask import redirect
from flask import url_for
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import NumberRange, DataRequired


from ..models import *
from ..util import *
from ..decorators import *


class UpdateCart(FlaskForm):
    '''
    Descripción: formulario de validación de UpdateCart. Valida pk y name
    '''
    pk = IntegerField('pk', validators=[NumberRange(min=0)])
    name = StringField('name', validators=[DataRequired()])


class AddToCart(UpdateCart):
    '''
    Parámetros: hereda de UpdateCart. Por lo tanto hace las validaciones
    de esa clase más las de su propia instancia.

    Descripción: formulario de validación de AddToCart. Valida quantity.
    '''
    quantity = IntegerField('quantity', validators=[NumberRange(min=1)])


def insert_atributes(producto):
    '''
    Parámetros: objeto Producto más las columnas añadidas en el router cart

    Descripción: añade al objeto su correspondiente imagen cover y calcula el
    precio total si se ha pedido más de un artículo.
    '''
    producto[0].total = producto[0].precio * producto[1]
    picture = get_product_cover(producto[0].id)
    if picture:
        producto[0].picture = picture


@app.route('/carrito/', methods=['GET'])
@login_required
def cart():
    '''
    Router: solo accesible mediante el método GET de HTTP/HTTPS.

    Descripción: cart Recupera la lista de todos los productos pertenecientes
    al carrito de un usuario. Concretamente el logueado y almacenado en la
    cookie de sesión.

    Función: renderiza la plantilla carrito.html con los parámetros: lista de
    productos, precio total de los productos y inicializa el formulario
    '''
    cart = Producto.query.join(Carro).filter(
            Carro.id_producto == Producto.id,
            Carro.id_usuario == get_user_id()
            ).add_columns(
                    Carro.cantidad,
                    ).all()

    total_price = 0

    for producto in cart:
        insert_atributes(producto)
        total_price += producto[0].total

    form = UpdateCart()

    return render_template('_views/carrito.html', productos=cart, total=total_price, form=form)


@app.route('/carrito/', methods=['POST'])
@login_required
def delete_all_cart():
    '''
    Router: solo accesible mediante el método POST de HTTP/HTTPS.

    Descripción: delete_all_cart emula la compra de los productos eliminandolos
    del carrito y almacenando en la tabla lista todos los productos del carrito
    con los atributos extra y la accion=comprado

    Función: redirecciona a index
    '''
    products = Carro.query.filter_by(id_usuario = get_user_id()).all()

    for cart in products:
        lista = Lista();
        lista.id_usuario = get_user_id()
        lista.id_producto = cart.id_producto
        lista.fecha = datetime.datetime.utcnow()
        lista.cantidad = cart.cantidad
        producto = Producto.query.get(cart.id_producto)
        lista.precio = producto.precio
        lista.accion = 'Comprado'

        db.session.add(lista)
        db.session.delete(cart)
        flash('Has eliminado {} del carrito'.format(
            producto.nombre), 'danger')

    db.session.commit()

    return make_response(redirect(url_for('index')))


@app.route('/carrito/add/', methods=['POST'])
@login_required
def add_cart():
    '''
    Router: solo accesible mediante el método POST de HTTP/HTTPS.

    Descripción: add_cart añade un producto al carrito que satisfaga
    las validaciones del formulario

    Función: redirecciona a cart
    '''
    form = AddToCart(request.form)
    quantity = form.data['quantity']
    pk = form.data['pk']
    name = form.data['name']

    if form.validate_on_submit():
        product = Carro()
        product.cantidad = quantity
        product.id_producto = pk
        product.id_usuario = get_user_id()
        db.session.add(product)

        db.session.commit()

        flash('Has añadido {} al carrito'.format(name), 'success')

    return make_response(redirect(url_for('cart')))


@app.route('/carrito/delete/', methods=['POST'])
@login_required
def delete_cart():
    '''
    Router: solo accesible mediante el método POST de HTTP/HTTPS.

    Descripción: delete_cart elimina un producto del carrito que satisfaga
    las validaciones del formulario

    Función: redirecciona a cart
    '''
    form = UpdateCart(request.form)
    pk = form.data['pk']
    name = form.data['name']

    if form.validate_on_submit():
        products = Carro.query.filter_by(
            id_usuario = get_user_id(),
            id_producto = pk,
            ).all()

        for cart in products:
            db.session.delete(cart)
            flash('Has eliminado {} del carrito'.format(name), 'danger')

        db.session.commit()

    return make_response(redirect(url_for('cart')))

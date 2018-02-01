#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sulushop import app
from flask import render_template

from models import *
from util import *
from decorators import *

from controllers.registro import *
from controllers.carrito import *
from controllers.login import *
from controllers.perfil import *
from controllers.detalle import *
from controllers.password import *


'''
Router: 	accesible mediante HTTP/HTTPS

Descripcion: 	Obtiene todos los productos de <page> de la base de datos y los preparamos para mostrarlos
                en html obteniendo a parte su imagen principal.

Funcion:	Lista todos los productos de la pagina en la que nos encontramos
'''
@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    lista = Producto.query.paginate(page, 20, False)
    form = AddToCart()
    for producto in lista.items:
        insert_atributes(producto)

    return render_template('_views/lista.html',
            productos=lista,
            form=form,)
'''
Descripcion: 	Busca en la base de datos la imagen principal de el producto y lo agrega a sus campos para
                el formateado en http.

Funcion:	Agrega a un producto un atributo con su imagen principal
'''
def insert_atributes(producto):
    picture = get_product_cover(producto.id)
    if picture:
        producto.picture = picture

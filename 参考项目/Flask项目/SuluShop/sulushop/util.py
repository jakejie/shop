#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sulushop import login_manager
import json
from flask import request

from models import *


@login_manager.user_loader
def load_user(user_id):
        return Usuario.get(user_id)


def get_user_cookie():
    """
    Descripción: Recupera la información almacenada en la cookie de sesion

    Función: retorna los datos de la cookie
    """
    try:
        data = json.loads(request.cookies.get('character'))
    except TypeError:
        data = {}
    return data


def get_user_id():
    """
    Descripción: Recupera el email del usuario almacenado en cookies,
    hace la consulta que devuelve el usuario que satisfaga email = e_mail

    Función: retorna el id del objeto usuario
    """
    e_mail = get_user_cookie()['email']

    user = Usuario.query.filter_by(email=e_mail).first()

    return user.id

def get_user_contrasena(e_mail):
    """
    Descripción: Recupera el email del usuario por parametro,
    hace la consulta que devuelve el usuario que satisfaga email = e_mail

    Función: retorna la contraseña del objeto usuario
    """
    user = Usuario.query.filter_by(email=e_mail).first()
    return user.contrasena

def get_user():
    """
    Descripción: Recupera el email del usuario almacenado en cookies,
    hace la consulta que devuelve el usuario que satisfaga email = e_mail

    Función: retorna en objeto usuario
    """
    e_mail = get_user_cookie()['email']

    user = Usuario.query.filter_by(email=e_mail).first()

    return user


def get_product_pictures(pk):
    """
    Parámetros: id de un producto

    Descripción: Pide una lista de fotos que cumpla pk = id_producot
    y id = id_foto

    Función: retorna una lista de fotos o []
    """
    picture = Foto.query.join(FotoProducto).filter(
            FotoProducto.id_producto == pk,
            FotoProducto.id_foto == Foto.id
            ).all()

    if not picture:
        return []

    return picture


def get_product_cover(pk):
    """
    Parámetros: id de un producto

    Descripción: Pide una foto que cumpla pk = id_producot y id = id_foto

    Función: retorna un string perteneciente a la url de la foto o []
    """
    picture = Foto.query.join(FotoProducto).filter(
            FotoProducto.id_producto == pk,
            FotoProducto.id_foto == Foto.id,
            ).first()

    if not picture:
        return []

    return picture.url


def get_action_list():
    """
    Descripción: Pide una lista de Productos que pertenezcan a la tabla
    lista

    Función: retorna una lista de producto perteneciente a la tabla lista
    """
    actions = Producto.query.join(Lista).filter(
            Lista.id_usuario == get_user_id()
            ).add_columns(Lista.fecha, Lista.accion).all()

    return actions


def get_favorite_list():
    """
    Descripción: Pide una lista de Productos que pertenezcan a la tabla
    lista y cumplan que el atributo accion sea igual a favorito

    Función: retorna lista de favoritos
    """
    favorites = Producto.query.join(Lista).filter(
            Lista.id_usuario == get_user_id(),
            Lista.accion == 'favorito',
            ).add_columns(Lista.fecha).all()

    return favorites

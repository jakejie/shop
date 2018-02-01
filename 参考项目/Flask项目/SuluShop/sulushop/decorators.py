#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request
from functools import wraps
from flask import redirect
from flask import url_for

from util import *


def login_required(f):
    """
    Parámetros: request

    Descripción: dependiendo si el usuario existe en las cookies redirecciona
    a login

    Función: redirecciona a login o sigue en el router del request
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_user_cookie():
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def logout_required(f):
    """
    Parámetros: request

    Descripción: dependiendo si el usuario existe en las cookies redirecciona
    a perfil

    Función: redirecciona a perfil o sigue en el router del request
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if get_user_cookie():
            return redirect(url_for('perfil', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

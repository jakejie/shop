from . import admin
from flask import render_template


@admin.route('/')
def index():
    return render_template('home_base.html')

# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Define the blueprint: 'home'
default = Blueprint('home', __name__)

# Set the route and accepted methods
@default.route('/home')
@default.route('/')
def index():
    return render_template("home/index.html")

# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

#import bootstrap
from flask_bootstrap import Bootstrap

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

#define bootstrap
bootstrap = Bootstrap(app)
# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module components using its blueprint handler variables
from app.add_stock.controllers import add_stock as addsk
from app.default.controllers import default as hm
from app.reports.controllers import reports as reps
from app.sales.controllers import sales as sale
from app.stock.controllers import stock as stk

# Register blueprint(s)
app.register_blueprint(addsk)
app.register_blueprint(hm)
app.register_blueprint(reps)
app.register_blueprint(sale)
app.register_blueprint(stk)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

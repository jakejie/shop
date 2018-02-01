# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for



# Import the database object from the main app module
from app import db

# Import module models (i.e. Stock and Purchase)
from app.models import Stock, Purchase, Sell

# Define the blueprint
reports = Blueprint('report', __name__)

# Set the route and accepted methods
@reports.route('/reports/')
def display():
    #retrieve all the reports
    purchase = Purchase.query.all()
    sell = Sell.query.all()
    return render_template("reports/report.html", sell = sell,purchase = purchase )

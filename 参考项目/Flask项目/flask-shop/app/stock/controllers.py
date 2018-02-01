# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import db

# Import module models (i.e. Stock and Purchase)
from app.models import Stock, Purchase

# Define the blueprint
stock = Blueprint('stock', __name__)

# Set the route and accepted methods
@stock.route('/stock/')
def viewStock():
    #reatrive all
    stock = Stock.query.all()
    return render_template("stock/stock.html", stock = stock)

@stock.route('/stock/item/<item_id>')
def viewItem(item_id):
    #retrieve current item
    item = Stock.query.filter_by(id=item_id).first()
    return render_template('stock/item.html', item = item)
@stock.route('/delete/<item_id>')
def delete(item_id):
    #delete current item
    dlt = Stock.query.filter_by(id=item_id).first()

    db.session.delete(dlt)
    db.session.commit()
    flash('product was successfully DELETED ')
    return redirect(url_for('stock.viewStock'))
@stock.route('/update/<item_id>')
def update(item_id):
    #update function
    item = Stock.query.filter_by(id=item_id).first()
    flash(' Update function not added ')
    return render_template('stock/item.html', item = item)

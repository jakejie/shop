# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for


# Import the database object from the main app module
from app import db

# Import module forms
from app.forms import AddStock

# Import module models (i.e. Stock and Purchase)
from app.models import Stock, Purchase

# Define the blueprint
add_stock = Blueprint('add', __name__, url_prefix='/add')

# Set the route and accepted methods
@add_stock.route('/stock/', methods=['GET', 'POST'])
def addStock():

    # If sign in form is submitted
    form = AddStock(request.form)

    # Verify the purchse form
    if form.validate_on_submit():
        # filter_by(name='')
        if Stock.query.filter_by(name=request.form['name']).first():

            updates = Stock.query.filter_by(name=request.form['name']).first()
            quantty = int(updates.quantity)
            qtty = int(request.form['quantity'])
            #update name
            updates.quantity = quantty + qtty

            #add to the purchase table
            pur_record = Purchase(request.form['name'], request.form['quantity'])
            db.session.add(pur_record)
            db.session.commit()
            flash('product was successfully updated ')
            return redirect(url_for('stock.viewItem', item_id = updates.id ))
        else:
            product = Stock(request.form['name'],
                                request.form['price'],
                                request.form['quantity'])
            #add to the purchase table
            pur_record = Purchase(request.form['name'], request.form['quantity'])
            db.session.add(product)
            db.session.add(pur_record)
            db.session.commit()
            flash('product was successfully added ')
            return redirect(url_for('stock.viewItem', item_id = product.id ))

    return render_template("add/add.html", form=form)

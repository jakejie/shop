# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for


# Import the database object from the main app module
from app import db

# Import module forms
from app.forms import sellItem

# Import module models
from app.models import Stock, Purchase, Sell

# Define the blueprint
sales = Blueprint('sell', __name__)

# Set the route and accepted methods
@sales.route('/sell/', methods=['GET', 'POST'])
def sell():

    form = sellItem(request.form)

    # Verify the sign in form
    if form.validate_on_submit():
        # filter_by(name='')
        if Stock.query.filter_by(name=request.form['name']).first():

            sell = Stock.query.filter_by(name=request.form['name']).first()
            quantty = int(sell.quantity)
            qtty = int(request.form['quantity'])
            #check for inconsistencies
            if quantty < qtty:
                flash('item out of stock,    >>>>>  %s items remaining'% (quantty) )
                return redirect(url_for('sell.sell'))
            if qtty == 0:
                flash('0 items cannot be sold' )
                return redirect(url_for('sell.sell'))
            sell.quantity = quantty - qtty
            #add to reports
            sell_record = Sell(request.form['name'], request.form['quantity'])
            db.session.add(sell_record)
            db.session.commit()
            flash('item was successfully sold ')
            return redirect(url_for('sell.sell'))
        else:
            flash('something went wrong ')
            return redirect(url_for('sell.sell'))

    return render_template("sales/sell.html", form=form)

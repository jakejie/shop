# Import Form and RecaptchaField (optional)
from flask_wtf import Form # , RecaptchaField

# Import Form elements such as TextField
from wtforms import TextField

# Import Form validators
from wtforms.validators import Required, EqualTo


# Define the add form (WTForms)

class AddStock(Form):
    name = TextField('name', [
                Required(message='Name')])

    price = TextField('price', [
                Required(message=' price')])

    quantity = TextField('quantity', [
                Required(message=' quantity')])

class sellItem(Form):
    name = TextField('name', [
                Required(message='Name')])
    quantity = TextField('quantity', [
                Required(message=' quantity')])

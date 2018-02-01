from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class CategoryForm(FlaskForm):
    categoryName = StringField('Category Name', validators=[DataRequired()], render_kw={"placeholder": "Category Name"})
    description = StringField('Description', widget=TextArea(), validators=[DataRequired()], render_kw={"placeholder": "Describe the category"})
    submit = SubmitField('Submit')


class ProductForm(FlaskForm):
	product_name = StringField('Product Name', validators=[DataRequired()], render_kw={'placeholder':'Product Name'})
	product_description =StringField('Product Description', validators=[DataRequired()])
	price = StringField('Price', validators=[DataRequired()])
	category_id = SelectField('Category', coerce=int)
	submit = SubmitField('Submit')


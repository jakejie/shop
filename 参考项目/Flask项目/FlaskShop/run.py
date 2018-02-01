'''
	if __name__ == "__main__":
    app.run(host='0.0.0.0')

'''
from shopApp import app, db
from shopApp.models import Category, Product, User


if __name__ == "__main__":
    app.run(host='0.0.0.0')


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Category': Category, 'Product': Product, 'User':User}
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from htmlmin.main import minify
from flask_login import LoginManager
from flask_compress import Compress
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


app = Flask(__name__)
app.secret_key = 'some_secret'

login_manager = LoginManager()
login_manager.init_app(app)
Compress(app)


app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://sulushop:1234sulushop@localhost/sulushop"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.after_request
def response_minify(response):
    """
    minify html response to decrease site traffic
    """
    if response.content_type == u'text/html; charset=utf-8':
        response.set_data(
            minify(response.get_data(as_text=True))
            )

        return response
    return response


import sulushop.views

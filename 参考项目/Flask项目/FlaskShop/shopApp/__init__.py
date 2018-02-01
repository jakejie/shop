from flask import Flask
from shopApp_config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_login import LoginManager


app = Flask(__name__)

#login manager object
login = LoginManager(app)

login.login_view = 'login'
#configuration object
app.config.from_object(app_config)

# flask sqlAlchemy and migrate
# Added this coz of the no alter error i kept getting
db = SQLAlchemy(app)
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate(app, db)
#migrate.init_app(app, db)
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


#Blueprint imports and registration
from shopApp.admin.views import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

from shopApp.home.views import home as home_blueprint
app.register_blueprint(home_blueprint)

from shopApp import models
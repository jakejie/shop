# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
# from fla import CsrfProtect
from flask_moment import Moment
from config import Config

db = SQLAlchemy()
bootstrap = Bootstrap()
# moment = Moment()
# 登陆管理
login_manager = LoginManager()
login_manager.session_protection = 'strong'
# 指定默认的登陆页面
login_manager.login_view = 'auth.login'


# static_folder = '',, static_url_path=''
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    # CsrfProtect(app)

    db.init_app(app)
    bootstrap.init_app(app)
    # moment.init_app(app)
    login_manager.init_app(app)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/admin")

    return app

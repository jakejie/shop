import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = 'roottoor'
    # PASSWORD = 'root'
    HOST = '59.110.230.99'
    # HOST = '127.0.0.1'
    PORT = 3306
    DATABASE = 'movie'

    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    ARTICLES_PER_PAGE = 10
    COMMENTS_PER_PAGE = 6
    SECRET_KEY = 'secret key to protect from csrf'
    WTF_CSRF_SECRET_KEY = 'random key for form'  # for csrf protection

    # Take good care of 'SECRET_KEY' and 'WTF_CSRF_SECRET_KEY', if you use the
    # bootstrap extension to create a form, it is Ok to use 'SECRET_KEY',
    # but when you use tha style like '{{ form.name.labey }}:{{ form.name() }}',
    # you must do this for yourself to use the wtf, more about this, you can
    # take a reference to the book <<Flask Framework Cookbook>>.
    # But the book only have the version of English.

    @staticmethod
    def init_app(app):
        pass

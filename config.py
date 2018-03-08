class Config():
    # 分页数据显示
    DATA_PER_PAGE = 6
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    # 验证邮箱配置
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "jakejie@163.com"
    MAIL_PASSWORD = "******"
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flask]'
    FLASKY_MAIL_SENDER = 'jakejie@163.com'
    # 数据库配置
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = 'roottoor'
    HOST = '******'
    PORT = 3306
    DATABASE = 'shopping'

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

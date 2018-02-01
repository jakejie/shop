import os

class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments
    SECRET_KEY = os.environ.get('SECRET_KEY') or '\xf92\xed\xf0\x9d\x13\x1e\xaf\x9d\xc4\x9fV\xfd\n\x11\xed|\xe2'
    basedir = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'shopApp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class app_config(Config):
    """
    Development configurations
    """

    DEBUG = True
    #SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

# app_config = {
#     'development': DevelopmentConfig,
#     'production': ProductionConfig
# }
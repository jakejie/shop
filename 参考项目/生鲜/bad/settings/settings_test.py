from settings.settings import *

REDIS_HOST = "redis"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'HOST': 'db',
        'USER': 'postgres',
        'PASSWORD': '',
        'PORT': 5432,
        'CONN_MAX_AGE': 30,
        'AUTOCOMMIT': True,
    }
}

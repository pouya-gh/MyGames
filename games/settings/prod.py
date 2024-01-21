from .base import *
import os

DEBUG = False

ADMINS = [
    ('Pouya Gharibpour', 'p.gharibpour@gmail.com'),
]

# ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': envrion_vars('MY_DB_NAME'),# 'mygames', #os.environ.get('POSTGRES_DB'),
        'USER': envrion_vars('MY_DB_USER'),#'postgres',# os.environ.get('POSTGRES_USER'),
        'PASSWORD': envrion_vars('MY_DB_PASSWORD'),#'tati71',# os.environ.get('POSTGRES_PASSWORD'),
        'HOST': envrion_vars('MY_DB_HOST'),#'localhost',
        # 'PORT': 5432,
    }
}

FILE_UPLOAD_HANDLERS = ['django.core.files.uploadhandler.TemporaryFileUploadHandler']
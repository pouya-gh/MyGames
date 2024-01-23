from .base import *

DEBUG = True

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'teststemp' / 'media'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'testsdb.sqlite3',
    }
}
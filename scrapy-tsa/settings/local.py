import json
import os
from .base import *

SECRET_KEY = 'v+0oiooho&!q0aa@zh)m)efpr=26hw25kev4p5x&v)#-_uocu&'
DB_NAME = "scrapy-tsa"

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, DB_NAME),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'scrapy-tsa',
        'USER': 'scrapy',
        'PASSWORD': 'scrapy',
        'HOST': 'localhost',
        'PORT': '5432',
    }

}

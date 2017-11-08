import json
import os
from .base import *

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
        'NAME': DB_NAME,
        'USER': 'postgres',
        'PASSWORD': 'local',
        'HOST': 'localhost',
        'PORT': '5432',
    }

}

import os
from .common import BASE_DIR

DEBUG = True

ALLOWED_HOSTS = ['localdev.com','127.0.0.1','localhost','192.168.2.248','106.75.24.32']

DOWNLOAD_HOST = 'http://localhost:8000' 

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
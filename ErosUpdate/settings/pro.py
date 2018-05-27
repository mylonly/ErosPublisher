DEBUG = False

ALLOWED_HOSTS = ['weex.1234tv.com']

DOWNLOAD_HOST = 'http://weexcdn.1234tv.com' 

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Weex',
        'USER': 'root'
    }
}
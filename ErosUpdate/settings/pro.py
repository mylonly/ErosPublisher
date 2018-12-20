DEBUG = True

ALLOWED_HOSTS = ['weex.1234tv.com']

DOWNLOAD_HOST = 'https://weexcdn.1234tv.com'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'weex',
        'USER': 'root',
        'PASSWORD': '1234TV.com'
    }
}

from .base import *

from django.conf import settings

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': settings.ENGINE,
        'NAME': settings.NAME_SCHEMA,
        'USER': settings.USERNAME,
        'PASSWORD': settings.PASSWORD,
        'HOST': settings.HOST,
        'PORT': settings.PORT,
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

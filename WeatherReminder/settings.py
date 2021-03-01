"""
Django settings for WeatherReminder project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os
import datetime
import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
load_dotenv()
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'main',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'WeatherReminder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'WeatherReminder.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.getenv('DB_NAME'),
    'USER': os.getenv('DB_USER'),
    'PORT': os.getenv('DB_PORT'),
    'HOST': os.getenv('DB_HOST'),
    'PASSWORD': os.getenv('DB_PASS')
}
}

'''DATABASES = {'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'weatherReminder',
    'USER': 'postgres',
    'PORT': '5432',
    'HOST': 'localhost',
    'PASSWORD': 'mirinda123'
}
}'''

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

django_heroku.settings(locals())
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=14),
}

TOKEN_URL = ''

if DEBUG:
    TOKEN_URL = 'https://weatherreminder.herokuapp.com/api/token/'
else:
    TOKEN_URL = 'http://127.0.0.1:8000/api/token/'

BROKER_URL = 'redis://:p82e1fe7b2e716174ce7ff15634d6665567eb6c87122a1a294b484ff7037f0bac@ec2-54-72-159-57.eu-west-1.compute.amazonaws.com:14179'
CELERY_RESULT_BACKEND = 'redis://:p82e1fe7b2e716174ce7ff15634d6665567eb6c87122a1a294b484ff7037f0bac@ec2-54-72-159-57.eu-west-1.compute.amazonaws.com:14179'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'bogdan.puziy@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
EMAIL_PORT = 465
EMAIL_USE_SSL = True

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

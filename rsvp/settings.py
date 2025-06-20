"""
Django settings for rsvp project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

from decouple import config

from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o*+hq=q9h0llzsw96(=*2*0kv9kz0g49o6bl9(40dk3uzza^4p'

# SECURITY WARNING: don't run with debug turned on in production!
try:
    DEBUG = config('DEBUG', default=True, cast=bool)
except Exception:
    DEBUG = True

APPEND_SLASH = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://rsvp.learn.fromindonesia.id', 'http://rsvp.learn.fromindonesia.id', 'http://localhost:8000', 'http://0.0.0.0:8000']

# Application definition

INSTALLED_APPS = [
    # django-unfold
    'unfold',
    # 'unfold.contrib.filters',
    # 'unfold.contrib.forms',
    # 'unfold.contrib.inlines',

    # built-in django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party
    'compressor', # django-compressor

    # Our App
    'app',
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

ROOT_URLCONF = 'rsvp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'rsvp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Auth
LOGIN_REDIRECT_URL = '/app/'

AUTHENTICATION_BACKENDS = ['app.auth.CustomAuthBackend']
AUTH_USER_MODEL = 'app.User'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



######################################################################
# Unfold
######################################################################
# UNFOLD = {
#     "SITE_HEADER": "RSVP Admin",
#     "SITE_TITLE": "RSVP Admin",
#     "SIDEBAR": {
#         "show_search": True,
#         "show_all_applications": True,
#         "navigation": [
#             {
#                 "title": "Navigation",
#                 "separator": False,
#                 "items": [
#                     {
#                         "title": "Users",
#                         "icon": "person",
#                         "link": reverse_lazy("admin:auth_user_changelist"),
#                     },
#                     {
#                         "title": "Groups",
#                         "icon": "label",
#                         "link": reverse_lazy("admin:auth_group_changelist"),
#                     },
#                 ],
#             },
#         ],
#     },
# }

######################################################################
# Compressor
######################################################################
COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', True)

COMPRESS_ROOT = BASE_DIR / 'static'

STATICFILES_FINDERS = ('compressor.finders.CompressorFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')

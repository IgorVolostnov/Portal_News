"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY_DJANGO"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_ORIGINS = ['http://*', 'https://*']
CSRF_TRUSTED_ORIGINS = ALLOWED_ORIGINS.copy()
ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # подключаем приложения для статичных страниц
    'django.contrib.sites',
    'django.contrib.flatpages',
    # подключаем приложение для новостей и статей
    'news',
    # создаем дополнительные поля для пользователей
    'fpages',
    'django_filters',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'NewsPaper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'NewsPaper.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ["NAME_PORTAL"],
        'USER': os.environ["USER_PORTAL"],
        'PASSWORD': os.environ["PASSWORD_PORTAL"],
        'HOST': os.environ["HOST_PORTAL"],
        'PORT': os.environ["PORT_PORTAL"],
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-ru'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
LOGIN_REDIRECT_URL = '/news/'
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
LOGIN_URL = '/accounts/login/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_ADAPTER = 'news.my_adapter.MyAccountAdapter'
ACCOUNT_FORMS = {'signup': 'news.forms.CommonSignupForm'}

SOCIALACCOUNT_PROVIDERS = {'yandex': {'EMAIL_AUTHENTICATION': True}}
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_ADAPTER = 'news.my_adapter.MySocialAccountAdapter'

ACCOUNT_SESSION_REMEMBER = True
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

SERVER_EMAIL = os.environ["EMAIL_ADDRESS_PORTAL_NEWS"]
DEFAULT_FROM_EMAIL = os.environ["EMAIL_ADDRESS_PORTAL_NEWS"]
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ["HOSTNAME_EMAIL_PORTAL_NEWS"]
EMAIL_PORT = os.environ["PORT_EMAIL_PORTAL_NEWS"]
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.environ["EMAIL_ADDRESS_PORTAL_NEWS"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_PASSWORD_PORTAL_NEWS"]
EMAIL_FILE_PATH = BASE_DIR / 'emails'
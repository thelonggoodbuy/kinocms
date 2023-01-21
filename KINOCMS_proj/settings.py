"""
Django settings for KINOCMS_proj project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import environ
import os
from django.utils.translation import gettext_lazy as _
from django.conf import global_settings



# env = environ.Env()
root = environ.Path(__file__)
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = int(env("DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
# ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(" ")
# ALLOWED_HOST = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
# ALLOWED_HOST = env("DJANGO_ALLOWED_HOSTS")



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'modeltranslation',
    'debug_toolbar',
    'bootstrap4',
    'phonenumber_field',
    'tempus_dominus',
    'django_cleanup.apps.CleanupConfig',
    'django_user_agents',

    'pages.apps.PagesConfig',
    'users.apps.UsersConfig',
    'cinema.apps.CinemaConfig',    
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'users.middleware.identify_user_device',
    # 'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'KINOCMS_proj.urls'

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
                'pages.processor.list_of_active_pages',
                'pages.processor.list_of_phones',
                'pages.processor.get_front_background_banner',
            ],
        },
    },
]

# TEMPLATE_CONTEXT_PROCESSORS = (
#     "pages.processor.list_of_active_pages",
# )


WSGI_APPLICATION = 'KINOCMS_proj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# CSRF_COOKIE_SAMESITE = 'Strict'
# CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS.copy()
# SESSION_COOKIE_SAMESITE = 'None'

# SESSION_COOKIE_SAMESITE = 'None'


# X_FRAME_OPTIONS = 'SAMEORIGIN'
# XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
    {
        'NAME': 'password_validators.NumberValidator', 
    },
]

# Authentication and authorization settings
AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_URL = '/users/sign_in/'
LOGOUT_REDIRECT_URL = '/users/sign_in/'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 7, }
    },
    { 'NAME': 'users.validators.NumberValidator', },
    { 'NAME': 'users.validators.UpercaseValidator', },
    { 'NAME': 'users.validators.LowercaseValidator', },
    { 'NAME': 'users.validators.SymbolValidator', },
]



# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'uk'
# LANGUAGE_CODE = "ru-RU"
MODELTRANSLATION_DEFAULT_LANGUAGE = 'uk'

# gettext = lambda s: s
LANGUAGES = (
    ("uk", _("Українська")),
    ("ru", _("Русский")),
)

MODELTRANSLATION_LANGUAGES = ('uk', 'ru')

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# location settings
PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'UA'


# FILE_UPLOAD_HANDLERS = [
#     'django.core.files.uploadhandler.TemporaryFileUploadHandler',
# ]


# media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



INTERNAL_IPS = [
    "127.0.0.1",
]

DATE_INPUT_FORMATS = ('%m/%d/%Y','%d-%m-%Y','%Y-%m-%d')

# templus dominus
TEMPUS_DOMINUS_LOCALIZE = True
# TEMPUS_DOMINUS_DATE_FORMAT = MM-DD-YY

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

DEFAULT_FROM_EMAIL = env('EMAIL_SENDING_DEFAULT_FROM_EMAIL')
EMAIL_USE_TLS = True
EMAIL_HOST = env('EMAIL_SENDING_EMAIL_HOST')
EMAIL_PORT = env('EMAIL_SENDING_EMAIL_PORT')
EMAIL_HOST_USER =  env('EMAIL_SENDING_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')


# CELERY settings
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
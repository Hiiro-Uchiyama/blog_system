## blog - ç - 2022 - Hiiro Uchiyama
## Edit 2021/12/28 - We have created an environment
## To rewrite the text in the template to blog.
## AWS databese
## The database needs to be changed.
## Improving the quality of content

from pathlib import Path
import dj_database_url
import os

## Build paths inside the project like this: BASE_DIR / 'subdir'.
## Quick-start development settings - unsuitable for production
## See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
## SECURITY WARNING: keep the secret key used in production secret!
## SECURITY WARNING: don't run with debug turned on in production!

## False for the production environment.
DEBUG = False

## Give priority to loading settings in local_settings.py
## Place local_settings.py in the same hierarchy.
## It must be written after DEBUG.

## Deployment destination information
## heroku login log.me.hiiro@gmail.com
## password ********** ********** **********
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'SECRET_KEY'

## Allowed domains
ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']

## If you want to add more applications, add them here
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog_app',
    'contact',
    'django_cleanup',
    'bootstrap4',
    'widget_tweaks',
    'django_summernote',
    'storages',
]

## WhiteNoiseMiddleware is required in the production environment.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'blog.urls'

## Setting up access to templates
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

WSGI_APPLICATION = 'blog.wsgi.application'

## https://docs.djangoproject.com/en/3.1/ref/settings/#databases
## If an error occurs on the local server
## sudo brew services start postgresql
## sudo brew services stop postgresql
## brew services restart postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'blog',
        'USER': 'USER',
        'PASSWORD': 'PASSWORD',
        'HOST': 'localhost',
        'PORT': '',
    }
}

## Database configuration for production environment
db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
DATABASES['default'].update(db_from_env)

## Password validation
## https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

## Internationalization
## https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

## Setting up AWS
## https://docs.djangoproject.com/en/3.1/howto/static-files/
AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'
AWS_STORAGE_BUCKET_NAME = 'AWS_STORAGE_BUCKET_NAME'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = S3_URL
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_EXPIRE = 63115200

## Specify a static file
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

## django-summernote
X_FRAME_OPTIONS = 'SAMEORIGIN'
SUMMERNOTE_THEME = 'bs4'
## Specify the character format of the file
FILE_CHARSET = 'utf-8'
## Specifying the number of pagination posts to display
PAGE_PER_ITEM = 10
## app.Comment: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

## upload file
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

## Google Mail settings
DEFAULT_FROM_EMAIL = 'DEFAULT_FROM_EMAIL'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'DEFAULT_FROM_EMAIL'
EMAIL_HOST_PASSWORD = 'EMAIL_HOST_PASSWORD'

## Processing when debugging is turned off
if not DEBUG:
    AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'
    AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'
    AWS_STORAGE_BUCKET_NAME = 'blog'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
    MEDIA_URL = S3_URL
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_EXPIRE = 63115200
    import django_heroku
    django_heroku.settings(locals())
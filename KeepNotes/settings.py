"""
Django settings for KeepNotes project.
Generated by 'django-admin startproject' using Django 3.1.4.
For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0^8z=hr@te=^2h@ggegr=#2qt#krf$111-vy-(y0kcim98v4m7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
AUTH_USER_MODEL = 'authentication.user'

# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'authentication',
    'Notes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_swagger',
    'drf_yasg',
  
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

ROOT_URLCONF = 'KeepNotes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/"templates"],
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

WSGI_APPLICATION = 'KeepNotes.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'keep_notes',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'keep_notes',
#         'USER': 'bharti',
#         'PASSWORD': 'bharti',
#         'PORT': '5432',

#     }
# }

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

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
REST_FRAMEWORK = {
     'DEFAULT_PERMISSION_CLASSES': [
         'rest_framework.permissions.IsAuthenticated',
         'rest_framework.permissions.IsAdminUser',
         ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
     'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
     )
}
# SWAGGER_SETTINGS = {
#     'SECURITY_DEFINITIONS': {
#         'Bearer': {
#             'type': 'apiKey',
#             'name': 'Authorization',
#             'in': 'header'
#         }
#     }

# }
# token=''
JWT_AUTH = {
   'JWT_ENCODE_HANDLER':
  'rest_framework_jwt.utils.jwt_encode_handler',
  'JWT_DECODE_HANDLER':
  'rest_framework_jwt.utils.jwt_decode_handler',
  'JWT_PAYLOAD_HANDLER':
  'rest_framework_jwt.utils.jwt_payload_handler',
  'JWT_PAYLOAD_GET_USER_ID_HANDLER':
  'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
  'JWT_RESPONSE_PAYLOAD_HANDLER':
  'rest_framework_jwt.utils.jwt_response_payload_handler',
 
  'JWT_SECRET_KEY': 'SECRET_KEY',
  'JWT_GET_USER_SECRET_KEY': None,
  'JWT_PUBLIC_KEY': None,
  'JWT_PRIVATE_KEY': None,
  'JWT_ALGORITHM': 'HS256',
  'JWT_VERIFY': True,
  'JWT_VERIFY_EXPIRATION': True,
  'JWT_LEEWAY': 0,
  'JWT_EXPIRATION_DELTA': datetime.timedelta(days=30),
  'JWT_AUDIENCE': None,
  'JWT_ISSUER': None,
  'JWT_ALLOW_REFRESH': False,
  'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30),
  'JWT_AUTH_HEADER_PREFIX': 'Bearer',
  'JWT_AUTH_COOKIE': None,
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'abc@gmail.com'
EMAIL_HOST_PASSWORD = '***'
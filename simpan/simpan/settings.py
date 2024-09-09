"""
Django settings for simpan project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import sys
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Set the environment variables.
env = environ.Env(
    # Django
    DEBUG=(bool, True),
    SECRET_KEY=(str, "django-insecure-4$@mf5t0@7#v6$ubbna$)gd)d_65l89zxr+c*#a_ysdxf0c)u&"),
    STATIC_BASE=(str, "static"),
    STATIC_ROOT=(str, "dist"),
    MEDIA_ROOT=(str, "media"),
    MEDIA_URL=(str, "/media/"),
    STATIC_URL=(str, "static/"),
    CELERY_BROKER_URL=(str, "amqp://guest:guest@localhost:5672//"),
    SUBMODULES_DIR=(str, "third_party"),
    LITEGRAPH_DIR=(str, "litegraph"),
    SDC_DIR=(str, "SDC"),
    LOG_LEVEL=(str, "INFO"),
    LOG_DIR=(str, "logs"),

    # Relational Database
    PGDATABASE=(str, "simpan"),
    PGUSER=(str, "simpan"),
    PGPASSWORD=(str, "simpan"),
    PGHOST=(str, "localhost"),
    PGPORT=(str, "5432"),

    # Langchain
    LANGCHAIN_TRACING_V2=(bool, True),
    LANGCHAIN_ENDPOINT=(str, "https://api.smith.langchain.com"),
    LANGCHAIN_API_KEY=(str, ""),
    LANGCHAIN_PROJECT=(str, "SimPan"),

    # Groq
    GROQ_API_KEY=(str, ""),

    # OpenAI
    OPENAI_API_KEY=(str, ""),
)

env_file = BASE_DIR / ".env"

if env_file.exists():
    env.read_env(env_file)

# Add to path the main project directory.
sys.path.append(str(BASE_DIR.parent)) # String representation of the posix path.

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',
    'drf_spectacular',
    'django_json_widget',

    # Apps
    'db.apps.DbConfig',
    'home.apps.HomeConfig',
    'comfyui.apps.ComfyuiConfig',
    'comfychat.apps.ComfychatConfig',
    'services.apps.ServicesConfig',
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

ROOT_URLCONF = 'simpan.urls'

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

WSGI_APPLICATION = 'simpan.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

'''
To install postgres using docker:

docker run -d --name postgres -p 5499:5432 \
-e POSTGRES_USER=simpan \
-e POSTGRES_PASSWORD=simpan \
-e POSTGRES_DB=simpan \
-v ./data/volumes/pg-data:/var/lib/postgresql/data \
postgres:latest

'''
# Use postgres.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("PGDATABASE"),
        'USER': env("PGUSER"),
        'PASSWORD': env("PGPASSWORD"),
        'HOST': env("PGHOST"),
        'PORT': env("PGPORT"),
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = env("STATIC_URL")
STATIC_BASE = env("STATIC_BASE")
STATICFILES_DIRS = [
    BASE_DIR / STATIC_BASE,
]
STATIC_ROOT = env("STATIC_ROOT")

# Media handling.
MEDIA_URL = env("MEDIA_URL")
MEDIA_ROOT = BASE_DIR / env("MEDIA_ROOT")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'SimPan API',
    'DESCRIPTION': 'API for SimPan project.',
    'VERSION': '1.0.0',
}

# Celery with rabbitmq configuration.
'''
To install rabbitmq using docker:
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management

http://host:15672 will show the rabbitmq management console.
http://host:5555 will show the flower monitoring console.
'''
CELERY_BROKER_URL = env("CELERY_BROKER_URL")

# Django Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] | [{asctime}] | [{module}] | [{process:d}] | [{thread:d}] | {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] | [{asctime}] | [{module}] | {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": env("LOG_LEVEL"),
            "class": "logging.FileHandler",
            "filename": BASE_DIR / env("LOG_DIR") / "simpan.log",
            "formatter": "verbose",
        },
        "console": {
            "level": env("LOG_LEVEL"),
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": env("LOG_LEVEL"),
            "propagate": True,
        },
        "db": {
            "handlers": ["file", "console"],
            "level": env("LOG_LEVEL"),
            "propagate": True,
        },
        "home": {
            "handlers": ["file", "console"],
            "level": env("LOG_LEVEL"),
            "propagate": True,
        },
        "comfyui": {
            "handlers": ["file", "console"],
            "level": env("LOG_LEVEL"),
            "propagate": True,
        },
        "comfychat": {
            "handlers": ["file", "console"],
            "level": env("LOG_LEVEL"),
            "propagate": True,
        },
        "services": {
            "handlers": ["file", "console"],
            "level": env("LOG_LEVEL"),
            "propagate": True,
        },
    },
}

# GIT Submodules
SUBMODULES_DIR = BASE_DIR.parent / env("SUBMODULES_DIR")
LITEGRAPH_DIR = env("LITEGRAPH_DIR")
SDC_DIR = env("SDC_DIR")
"""
Django settings for base project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
from urlparse import urlparse, uses_netloc

##
#
# Debug Flags
#
##
def boolcheck(s):
    if isinstance(s, basestring):
        return s.lower() in ("true", "yes", "t", "1")
    else:
        return bool(s)


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


DEBUG = boolcheck(os.environ.get('DEBUG', False))
TEMPLATE_DEBUG = DEBUG
DEBUG_TOOLBAR = boolcheck(os.environ.get('DEBUG_TOOLBAR', DEBUG))


if DEBUG==False:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = []



# SECURITY WARNING: keep the secret key used in production secret!
# Secret key should be the same on all of your servers. You can put it directly into settings if that is safe for you. Or you can specify it as an environment variable.
# Get one here: http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = os.environ.get('SECRET_KEY', '6v-*o2qnkr!xr$y&yrgosxoup%*y)x2!sr5@-&^dmqtx7)c0tj')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gunicorn'
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


JINGO_EXCLUDE_APPS = []

ROOT_URLCONF = 'base.urls'
WSGI_APPLICATION = 'base.wsgi.application'


#################################################
# Parse database configuration from $DATABASE_URL
#################################################
# if 'DATABASE_URL' does no exist then use sqllite from file
if not os.environ.has_key('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:////'+os.path.join(BASE_DIR, 'db.sqlite3')

import dj_database_url
DATABASES = {'default': dj_database_url.config(default=os.environ['DATABASE_URL'])}


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
#Added from Heroku instructions
STATIC_ROOT = BASE_DIR+'/staticfiles'
STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR , 'templates').replace('\\','/'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

##
#
# Debug Toolbar
#
##
def debug_toolbar_available():
    try:
        import debug_toolbar
        return True
    except ImportError:
        return False

if DEBUG_TOOLBAR and debug_toolbar_available():
    MIDDLEWARE_CLASSES.insert(0,'debug_toolbar.middleware.DebugToolbarMiddleware')
    INSTALLED_APPS.append('debug_toolbar')
    INTERNAL_IPS = (
    '127.0.0.1',
    )
    JINGO_EXCLUDE_APPS.append('debug_toolbar')
    CONFIG_DEFAULTS = {
        # Toolbar options
        'RESULTS_STORE_SIZE': 3,
        'SHOW_COLLAPSED': True,
        # Panel options
        'INTERCEPT_REDIRECTS': False,
        'SQL_WARNING_THRESHOLD': 100,   # milliseconds
    }


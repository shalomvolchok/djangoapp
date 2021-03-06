"""
Django settings for base project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
from urlparse import urlparse, uses_netloc
import sys

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


DEBUG = boolcheck(os.environ.get('DEBUG', True))

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
# TESTING SETUP
#
##
if DEBUG:
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    NOSE_ARGS = [#'--nocapture',
                 #'--nologcapture',
                 #'--with-coverage',
                 #'--cover-package=assembler',
                 #'--cover-html',
                 '--logging-level=DEBUG'
                 ]

else:
    TEST_RUNNER = 'base.utils.fasttestrunner.FastTestRunner'

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

if len(sys.argv) > 1 and sys.argv[1] != 'test':
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
        DEBUG_TOOLBAR_PANELS = [
               'debug_toolbar.panels.versions.VersionsPanel',
               'debug_toolbar.panels.timer.TimerPanel',
               'debug_toolbar.panels.settings.SettingsPanel',
               'debug_toolbar.panels.headers.HeadersPanel',
               'debug_toolbar.panels.request.RequestPanel',
               'debug_toolbar.panels.sql.SQLPanel',
               'debug_toolbar.panels.staticfiles.StaticFilesPanel',
               'debug_toolbar.panels.templates.TemplatesPanel',
               'debug_toolbar.panels.cache.CachePanel',
               'debug_toolbar.panels.signals.SignalsPanel',
               'debug_toolbar.panels.logging.LoggingPanel',
               'debug_toolbar.panels.redirects.RedirectsPanel',
           ]  
        #template timings panel
        INSTALLED_APPS.append('template_timings_panel')
        DEBUG_TOOLBAR_PANELS.append('template_timings_panel.panels.TemplateTimings.TemplateTimings')
        IGNORED_TEMPLATES = ["debug_toolbar/*"] # Ignore these templates from the output        


##
#
# Logging settings
#
##
else:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            }            
        },
        'handlers': {
            'null': {
                'class':'django.utils.log.NullHandler',
                'level': 'DEBUG',            
            },
            'console':{
                'level': 'INFO',
                'filters': ['require_debug_true'],            
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },      
            'development_console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],            
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },                          
            'development_logfile': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.FileHandler',
                'filename': BASE_DIR+'/logs/django.log',
                'formatter': 'verbose'
            },
            'production_logfile': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'logging.FileHandler',
                'filename': BASE_DIR+'/logs/django_production.log',
                'formatter': 'simple'
            },
            'production_dba_logfile': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'logging.FileHandler',
                'filename': BASE_DIR+'/logs/django_production_dba.log',
                'formatter': 'simple'
            },                                 
        },
        'root':{
                'handlers': ['development_console'],
                'level': 'DEBUG',
        },
        'loggers': {
            '': {
                'handlers': ['development_console','development_logfile','production_logfile'],
                'level': 'DEBUG', 
                'propagate': True,
             },
            'dba': {
                'handlers': ['console','production_dba_logfile'],
            },                      
           'django.request': {
                'handlers': ['development_logfile','production_logfile'],
                'propagate': False,
            },
            'django': {
                'handlers': ['null'],
                'propagate': True,
                'level': 'INFO',
            },                
        }
    }


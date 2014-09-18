"""
Django settings for djdam project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MEDIA_ROOT = os.path.join(BASE_DIR, 'var','media')
if os.path.isdir(MEDIA_ROOT):
    pass
else:
    os.makedirs(MEDIA_ROOT, mode=0777)

STATIC_ROOT= os.path.join(BASE_DIR, 'var','static')
if os.path.isdir(STATIC_ROOT):
    pass
else:
    os.makedirs(STATIC_ROOT, mode=0777)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_URL = '/media/'
STATIC_URL = '/static/'


SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'quu&b1+7x+h511z5u&yfu)%9-^px86rzjuahd$t&1)iqepxz#l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
# All hosts allowed
ALLOWED_HOSTS = ['*']
# No hosts allowed
# ALLOWED_HOSTS = []

## Must be set for Debug toolbar
INTERNAL_IPs = ('127.0.0.1',)


# Application definition

INSTALLED_APPS = (# '',
    # 'admin_bootstrap',
    # # DjangoAdminBootstrapped
    'django_admin_bootstrapped',
    # Dj Admin Tools
    #'admin_tools',  #
    #'admin_tools.theming',  #
    #'admin_tools.dashboard',  #
    #'admin_tools.menu',
    #'adminactions',  #
    # Django contrib apps/admin
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admindocs',
    #'django.contrib.markup',
    'django.contrib.humanize',
    'django.contrib.syndication',
    'django.contrib.staticfiles',
    'django.contrib.redirects',
    # Third-party apps, patches, fixes
    'djcelery',  #
    'debug_toolbar',  #
    'compressor',
    #'debug_toolbar_user_panel',#

    # bootstrap and other toolkits for widgets tables forms etc.
    'bootstrap3',
    'bootstrap_toolkit',
    'crispy_forms',
    'django_tables2',
    'django_filters',
    # 'floppyforms',

    # Database migrations
    'south',

    # Gunicorn and Servers
    'gunicorn',

    # Image/Thumbnail Rendering and Manipulation
    # 'sorl.thumbnail',
    # 'ajaxuploader',
    # 'ajax_upload',

    ## REST
    'rest_framework',
    'tastypie',

    # Application base, containing global templates and Home Page View
    'base',

    # Local apps, referenced via appname
    'searcher',
    'imgadjust',
    # 'uploader',
    # 'accounts',

    # Local digassets app, referenced via appname
    #'digassets',

    # Local ajaxsearch app, referenced via appname
    'ajaxsearch',
    'ajax_select',
    #'autocomplete',
)

ROOT_URLCONF = 'djdam.urls'

WSGI_APPLICATION = 'djdam.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'www_django',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': '127.0.0.1',
        'PORT': '3301',
        #'OPTIONS': {
        #    'init_command': 'SET storage_engine=InnoDB',
        #    'charset' : 'utf8',
        #    'use_unicode' : True,
        #},
        #'TEST_CHARSET': 'utf8',
        #'TEST_COLLATION': 'utf8_general_ci',
    },
    # 'slave': {
    #     ...
    # },
}

# Uncomment this and set to all slave DBs in use on the site.
# SLAVE_DATABASES = ['slave']

################## EMAIL SETTINGS AND LOCAL ADMIN ######################
# Recipients of traceback emails and other notifications.
ADMINS = (
    ('johnb', 'john.bragato@gmail.com'),
)
MANAGERS = ADMINS

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'searcher.utils.Tastypie_Default_Format.TastyJSONMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'templates/searcher'),
    os.path.join(BASE_DIR, 'templates/uploader'),
    os.path.join(BASE_DIR, 'templates/ajaxsearch'),
    os.path.join(BASE_DIR, 'templates/accounts'),
    os.path.join(BASE_DIR, 'templates/imgadjust'),
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'john.bragato@gmail.com'
# EMAIL_FILE_PATH =
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '993'
EMAIL_HOST_USER = 'john.bragato@gmail.com'
EMAIL_HOST_PASSWORD = ''



#####################################################################
#################  SORL.THUMBNAIL & REDIS SERVER SETUP  #############
#####################################################################
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:1',
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        }
    }
}


THUMBNAIL_FORMAT = 'PNG'
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_REDIS_HOST = '127.0.0.1' # default
THUMBNAIL_REDIS_PORT = 6379 # default
THUMBNAIL_DEBUG = True
THUMBNAIL_QUALITY = 60
THUMBNAIL_PROGRESSIVE = False

FILE_UPLOAD_TEMP_DIR = '/var/tmp/'
#FILE_UPLOAD_TEMP_DIR = '/tmp'
FILE_UPLOAD_MAX_MEMORY_SIZE = 157286400

#####################################################################
#####       Storage/Cache Services
#####################################################################
#AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
#AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
#AWS_STORAGE_BUCKET_NAME = '<YOUR BUCKET NAME>'

#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'


# Log settings
import logging
logging.basicConfig()
log = logging.getLogger(__name__)

LOG_LEVEL = logging.INFO
HAS_SYSLOG = True

SYSLOG_TAG = "http_app_djdam"  # Make this unique to your project.

# Remove this configuration variable to use your custom logging configuration
LOGGING_CONFIG = None
LOGGING = {
   'version': 1,
   'loggers': {
       'djdam': {
           'level': "DEBUG"
       }
   }
}

# Place bcrypt first in the list, so it will be the default password hashing
# mechanism
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

# Sessions
#
# By default, be at least somewhat secure with our session cookies.
SESSION_COOKIE_HTTPONLY = True

# Set this to true if you are using https
SESSION_COOKIE_SECURE = False

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
# from django.core.exceptions import ImproperlyConfigured
#
#
# def get_env_setting(setting):
#     """ Get the environment setting or return exception """
#     try:
#         return os.environ[setting]
#     except KeyError:
#         error_msg = "Set the %s env variable" % setting
#         raise ImproperlyConfigured(error_msg)


# Specify a custom user model to use
#AUTH_USER_MODEL = 'accounts.djdamUser'
# SECURITY WARNING: keep the secret key used in production secret!
# Hardcoded values can leak through source control.
# This is an example method of getting the value from an environment setting.
# Uncomment to use, and then make sure you set the SECRET_KEY environment variable.
# This is good to use in production, and on services that support it such as Heroku.
#SECRET_KEY = get_env_setting('SECRET_KEY')



#==============================================================================
#  Celery settings
#==============================================================================
# import djcelery
# celery.setup loader()
# BROKER_URL = "django://"
# Uncomment these to activate and customize Celery:
# CELERY_ALWAYS_EAGER = False  # required to activate celeryd
# BROKER_HOST = 'localhost'
# BROKER_PORT = 5672
# BROKER_USER = 'django'
# BROKER_PASSWORD = 'django'
# BROKER_VHOST = 'django'
# CELERY_RESULT_BACKEND = 'amqp'


# Enable these options for memcached
CACHE_BACKEND= "memcached://127.0.0.1:11211/"
CACHE_MIDDLEWARE_ANONYMOUS_ONLY=True

# Set this to true if you use a proxy that sets X-Forwarded-Host
USE_X_FORWARDED_HOST = True

#==============================================================================
#  Project Email settings
#==============================================================================

SERVER_EMAIL = "johnb@prodimages.ny.bluefly.com"
DEFAULT_FROM_EMAIL = "johnb@prodimages.ny.bluefly.com"
SYSTEM_EMAIL_PREFIX = "[prodimages.ny.bluefly.com]"

#==============================================================================
# Miscellaneous project settings
#==============================================================================

# Global Upload File Perms
FILE_UPLOAD_PERMISSIONS = 0664
# FILE_UPLOAD_PERMISSIONS = 1777

#==============================================================================
# Third party app settings
#==============================================================================
# List of callables that know how to import templates from various sources.


def custom_show_toolbar(request):
    """ Only show the debug toolbar to users with the superuser flag. """
    return request.user.is_superuser

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    'HIDE_DJANGO_SQL': False,
    'TAG': 'body',
    'SHOW_TEMPLATE_CONTEXT': True,
    'ENABLE_STACKTRACES': True,
}
#
DEBUG_TOOLBAR_PANELS = (
    #'debug_toolbar_user_panel.panels.UserPanel',
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    #'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    #'debug_toolbar.panels.logger.LoggingPanel',

)


#
## Customize Admin interface with Admin Tools
#ADMIN_TOOLS_MENU = 'menu.CustomMenu'
#ADMIN_TOOLS_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'
## ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'dashboard.CustomAppIndexDashboard'
ADMIN_TOOLS_THEMING_CSS = 'css/theming.css'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

## REST FRAMEWORK SETTINGS
TASTYPIE_DEFAULT_FORMATS = ['json']
API_LIMIT_PER_PAGE = 20

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY': 20
}


### AUTOCOMPLETE django-ajax-selects
# define the lookup channels in use on the site
# AJAX_LOOKUP_CHANNELS = {
#     #  simple: search Person.objects.filter(name__icontains=q)
#     'person'  : {'model': 'example.person', 'search_field': 'name'},
#     # define a custom lookup channel
#     'song'   : ('example.lookups', 'SongLookup')
# }

from __future__ import with_statement
from os import path

#
# Configuration file must contain:
#
# DEBUG
# DATABASE_ENGINE
# DATABASE_NAME
# DATABASE_USER
# DATABASE_PASSWORD
# DATABASE_HOST
# DATABASE_PORT
# SECRET_KEY
# TIME_ZONE
# LANGUAGE_CODE
# USE_I18N
# EMAIL_HOST
# EMAIL_PORT
# DEFAULT_FROM_EMAIL
# ADMINS
#
# See Django documentation for possible values.
#

try:
    with open('/etc/femtec-2011.conf', 'r') as conf:
        exec conf.read()
except IOError:
    BASE_PATH            = path.expanduser('~/tmp/femtec-2011')
    DEBUG                = True
    DATABASE_ENGINE      = 'sqlite3'
    DATABASE_NAME        = path.join(BASE_PATH, 'femtec-2011.db')
    DATABASE_USER        = ''
    DATABASE_PASSWORD    = ''
    DATABASE_HOST        = ''
    DATABASE_PORT        = ''
    SECRET_KEY           = 'Hokjzn_r-no1q&!!u73-qwt0*ea8i^0r65ydeh$@kyj&^_0q$e'
    TIME_ZONE            = 'US/Pacific'
    LANGUAGE_CODE        = 'en-us'
    ADMINS               = ()
    ABSTRACTS_PATH       = path.join(BASE_PATH, 'abstracts')
    EMAIL_HOST           = 'smtp.unr.edu'
    EMAIL_PORT           = 25
    EMAIL_SUBJECT_PREFIX = ''
    DEFAULT_FROM_EMAIL   = 'femtec2011-noreply@unr.edu'
    SERVER_EMAIL         = DEFAULT_FROM_EMAIL

TEMPLATE_DEBUG = DEBUG
MANAGERS = ADMINS

SITE_ID = 1

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'femtec.contrib.nocache.NoCacheIfAuthenticatedMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'femtec.site',
)

ROOT_URLCONF = 'femtec.urls'

TEMPLATE_DIRS = (
    path.join(path.dirname(__file__), 'templates'),
)

MEDIA_ROOT = path.join(path.dirname(__file__), 'media')
MEDIA_URL  = '/events/femtec-2011/media/'
LOGIN_URL  = '/events/femtec-2011/account/login/'

ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'

DEFAULT_CONTENT_TYPE = 'text/html'

MIN_PASSWORD_LEN = 6
CHECK_STRENGTH = True

CAPTCHA = {
    'fgcolor': '#254b6f',
    'imagesize': (200, 50),
}

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
AUTH_PROFILE_MODULE = 'site.UserProfile'

AUTHENTICATION_BACKENDS = (
    'femtec.contrib.emailauth.EmailBackend',
)


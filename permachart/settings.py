import os

PROJECT_ROOT = os.path.dirname(__file__)
DEBUG = False
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('Justin Lilly', 'justin+permachart@justinlilly.com'),
)
MANAGERS = ADMINS
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
MEDIA_ROOT = ''
MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = '5343xe*^^nc69qa%khwav1)dq^&s2bfa#oc_hm2p#zl$z-x+l*'
ROOT_URLCONF = 'permachart.urls'
DATABASE_ENGINE = ''
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    # FIXME: add csrf protection
)
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'charter',
)
TEMPLATE_CONTEXT_PROCESSORS = (
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
)
TEMPLATE_DIRS = os.path.join(PROJECT_ROOT, 'templates')

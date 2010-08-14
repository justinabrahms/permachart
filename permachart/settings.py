import os

PROJECT_ROOT = os.path.dirname(__file__)
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Justin Lilly', 'justin+permachart@justinlilly.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': '', 
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = '5343xe*^^nc69qa%khwav1)dq^&s2bfa#oc_hm2p#zl$z-x+l*'
ROOT_URLCONF = 'permachart.urls'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.messages',
)
TEMPLATE_DIRS = os.path.join(PROJECT_ROOT, 'templates')

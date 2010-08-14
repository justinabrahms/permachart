import logging, os, sys

# unfuck pdb
for attr in ('stdin', 'stdout', 'stderr'):
    setattr(sys, attr, getattr(sys, '__%s__' % attr))

# Google App Engine imports.
from google.appengine.ext.webapp import util

# # Remove the standard version of Django.
for k in [k for k in sys.modules if k.startswith('django')]:
    del sys.modules[k]

# # Force sys.path to have our own directory first, in case we want to import
# # from it.
BASE_PATH = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(BASE_PATH))
for path, dirs, files in os.walk(os.path.join(BASE_PATH, 'deps')):
    for dir in dirs:
        sys.path.insert(0, os.path.join(path, dir))
sys.path.insert(0, os.path.join(BASE_PATH, 'permachart'))

# Must set this env var *before* importing any part of Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'permachart.settings'

import django.core.handlers.wsgi
import django.core.signals

def log_exception(*args, **kwds):
   logging.exception('Exception in request:')

# Log errors.
django.core.signals.got_request_exception.connect(log_exception)

def main():
    application = django.core.handlers.wsgi.WSGIHandler()
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

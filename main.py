import logging, os, sys

# Google App Engine imports.
from google.appengine.ext.webapp import util

# # Remove the standard version of Django.
for k in [k for k in sys.modules if k.startswith('django')]:
    del sys.modules[k]

# # Force sys.path to have our own directory first, in case we want to import
# # from it.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
for path, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), 'deps')):
    for dir in dirs:
        sys.path.insert(0, os.path.join(path, dir))

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

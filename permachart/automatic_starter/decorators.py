from django.http import HttpResponseRedirect, Http404, HttpResponse
from google.appengine.api import users

def login_required(func):
    def _wrap(request, *args, **kwargs):
        user = users.get_current_user()
        if not user:
            return HttpResponseRedirect(users.create_login_url(request.build_absolute_uri()))
        request.g_app_user = user
        return func(request, *args, **kwargs)
    _wrap.__doc__ = func.__doc__
    _wrap.__name__ = func.__name__
    return _wrap

def user_in_request(func):
    def _wrap(request, *args, **kwargs):
        user = users.get_current_user()
        if not user:
            request.g_app_user = None
        request.g_app_user = user
        return func(request, *args, **kwargs)
    _wrap.__doc__ = func.__doc__
    _wrap.__name__ = func.__name__
    return _wrap
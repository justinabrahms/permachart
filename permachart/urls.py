from django.conf.urls.defaults import *
from charter import views as charter_views

urlpatterns = patterns(
    '',
    url('^$', charter_views.home, name="home"),
    url('^new/$', charter_views.manual_data_import, name="new-chart"),
)

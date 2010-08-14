from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from charter import views as charter_views

urlpatterns = patterns(
    '',
    url('^$', direct_to_template, {'template': 'home.html'}, name="home"),
    url('^new/$', charter_views.manual_data_import, name="chart-new"),
    url('^(.*)/$', charter_views.chart_detail, name="chart-detail"),
)

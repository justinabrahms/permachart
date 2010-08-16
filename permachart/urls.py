from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from charter import views as charter_views

urlpatterns = patterns(
    '',
    url('^$', direct_to_template, {'template': 'home.html'}, name="home"),
    url('^new/$', charter_views.manual_data_import, name="chart-new"),
    url('^list/$', charter_views.chart_list, name="chart-list"),
    url('^tmp-data/$', charter_views.pop_data),
    url('^oembed/$', charter_views.oembed, name='oembed'),
    url('^chart/([-\w]+)/$', charter_views.chart_resource, name="chart-resource"),
    url('^(.*)/edit/$', charter_views.data_edit, name="chart-data-edit"),
    url('^([-\w]+)/([-\w]+)/$', charter_views.chart_detail_version, name="chart-detail-version"),
    url('^([-\w]+)/$', charter_views.chart_detail, name="chart-detail"),
)

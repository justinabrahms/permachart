from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response
from google.appengine.ext import db
from google.appengine.api import users

from charter.models import Chart, ChartDataSet, DataRow
from charter.forms import ChartForm
from charter.utils import _cht, get_graph_url


def get_object_or_404(cls, **kwargs):
    try:
        obj = cls.get(**kwargs)
    except:
        raise Http404

def signin(request):
    # likely handled by appengine, but might require a callback?
    pass

def manual_data_import(request):
    if request.method == "POST":
        cf = ChartForm(request.POST)
        if cf.is_valid():
            chart = cf.save()
            return HttpResponseRedirect(reverse('chart-detail', args=(chart.hash,)))
    else:
        cf = ChartForm()
    return render_to_response('charter/data_input.html', {'f':cf})

def data_edit(request, hash):
    chart = Chart.get()

def bulk_data_import(request):
    pass

def chart_detail(request, hash):
    chart = get_object_or_404(Chart, hash=hash)
    graph = get_graph_url(chart.data, _cht[chart.chart_type])
    return render_to_response('charter/detail.html', {'chart':chart, 'graph': graph})

def chart_list(request):
    chart_list = Chart.all()
    return render_to_response('charter/list.html', {'chart_list':chart_list})

def get_chart_resource(request):
    pass

def pop_data(request):
    import time, random
    dr = DataRow(data_key="asdf", data_value=str(random.randint(0,1000)))
    dr_key = dr.save()
    dr2 = DataRow(data_key="asdf", data_value=str(random.randint(0,1000)))
    dr2_key = dr2.save()
    cds = ChartDataSet(version=1, data_rows=[dr_key])
    cds.save()
    cds2 = ChartDataSet(version=2, previous_version=cds, data=[dr2_key])
    cds2.save()
    c = Chart(name='%s' % time.time(), chart_type="pie", data=cds2)
    c.hash = c.get_hash()
    c.save()
    return HttpResponse('success')

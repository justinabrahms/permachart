from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response
from google.appengine.ext import db
from google.appengine.api import users

from charter.models import Chart, ChartDataSet, DataRow
from charter.forms import ChartForm, DataSetForm, DataRowForm, DataRowFormSet
from charter.utils import _cht, get_graph, pretty_decode
from urlparse import urlparse
from django.utils import simplejson as json

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
        return HttpResponseRedirect(reverse('chart-data-edit', args=(chart.get_hash(),)))
    else:
        cf = ChartForm()
    return render_to_response('charter/data_input.html', {'f':cf})

def data_edit(request, hash):
    chart = Chart.get_by_id(pretty_decode(hash))
    if request.method == "POST":
        old_dataset = chart.data or None
        if chart.data:
            fs = DataRowFormSet(data=request.POST, instances=chart.data.data_rows)
        else:
            fs = DataRowFormSet(data=request.POST)
        if fs.is_valid():
            keys = []
            for form in fs.forms:
                if hasattr(form, 'cleaned_data'):
                    dr = DataRow(**form.cleaned_data)
                    keys.append(dr.save())
            version = old_dataset.version + 1 if old_dataset else 1
            cds = ChartDataSet(version = version,
                               previous_version = old_dataset,
                               data_rows = keys)
            cds.save()
            chart.data = cds
            chart.save()
            return HttpResponseRedirect(reverse('chart-detail', args=(chart.get_hash(),)))
    else:
        if chart.data:
            fs = DataRowFormSet(instances=chart.data.data_rows)
        else:
            fs = DataRowFormSet()
    return render_to_response('charter/data_edit.html', {'formset': fs})

def bulk_data_import(request):
    pass

def chart_detail(request, hash):
    chart = Chart.get_by_id(pretty_decode(hash))
    if chart.data:
        graph_url, graph = get_graph(chart.data, _cht[chart.chart_type])
    else:
        graph_url, graph = None, None
    return render_to_response('charter/detail.html', {
        'chart':chart, 
        'graph': graph,
        'graph_url': graph_url,
        'version': chart.data
    })

def chart_detail_version(request, hash, version_key):
    chart = Chart.get_by_id(pretty_decode(hash))
    version = ChartDataSet.get(version_key)
    graph_url, graph = get_graph(version, _cht[chart.chart_type])
    return render_to_response('charter/detail.html', {
        'chart':chart,
        'graph': graph,
        'graph_url': graph_url,
        'version': version,
        'version_specific': True
    })

def chart_list(request):
    chart_list = Chart.all()
    return render_to_response('charter/list.html', {'chart_list':chart_list})

def get_chart_resource(request):
    pass
    
def oembed(request):
    if not request.GET.get('url'):
        return HttpResponse('{"error":"No Url Provided."}')
    url_parts = urlparse(request.GET.get('url'))
    keys = url_parts.path.split('/')
    for key in range(len(keys)):
        if len(keys[key]) and keys[key][-1] == '+': #stats
            keys[key] = keys[key][:-1]
    chart = Chart.get(keys[1])
    if len(keys) > 3:
        version = ChartDataSet.get(keys[2])
        perma = reverse('chart-detail-version', args=(keys[1], keys[2]))
    else:
        version = chart.data
        perma = reverse('chart-detail', args=(keys[1], ))
    graph_url, graph = get_graph(version, _cht[chart.chart_type], 600, 480)
    oembed = {
        "version": str(version.version),
        "type": "photo",
        "width": 600,
        "height": 480,
        "title": chart.name,
        "url": graph_url,
        "provider_name": "Permachart",
        "provier_url": "http://permachart.appengine.com"
    }
    return HttpResponse(json.dumps(oembed))

def pop_data(request):
    import time, random
    dr = DataRow(data_key="asdf", data_value=str(random.randint(0,1000)))
    dr_key = dr.put()
    dr2 = DataRow(data_key="asdf2", data_value=str(random.randint(0,1000)))
    dr2_key = dr2.put()
    dr3 = DataRow(data_key="asdf2", data_value=str(random.randint(0,1000)))
    dr3_key = dr3.put()
    cds = ChartDataSet(version=1, data_rows=[dr_key, dr2_key])
    cds.put()
    cds2 = ChartDataSet(version=2, previous_version=cds, data_rows=[dr_key, dr3_key])
    cds2.put()
    c = Chart(name='%s' % time.time(), chart_type="pie", data=cds2)
    c.put()
    return HttpResponse('success')

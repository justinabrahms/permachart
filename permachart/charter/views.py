from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from google.appengine.ext import db
from google.appengine.api import users

from charter.models import Chart, ChartDataSet, DataRow
from charter.forms import ChartForm

def home(request):
    return render_to_response('home.html')

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

def bulk_data_import(request):
    pass

def chart_detail(request, hash):
    try:
        chart = Chart.get(hash=hash)
    except:
        raise Http404
    return render_to_response('charter/detail.html', {'chart':chart})

def chart_list(request):
    chart_list = Chart.all()
    return render_to_response('charter/list.html', {'chart_list':chart_list})

def get_chart_resource(request):
    pass

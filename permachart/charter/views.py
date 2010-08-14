from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from google.appengine.ext import db

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
            ident = cf.save()
            return HttpResponseRedirect(reverse('chart-detail', args=(ident.key(),)))
    else:
        cf = ChartForm()
    return render_to_response('charter/data_input.html', {'f':cf})

def bulk_data_import(request):
    pass

def chart_detail(request, id):
    chart = Chart.get(id)
    return render_to_response('charter/detail.html', {'chart':chart})


def chart_list(request):
    pass

def get_chart_resource(request):
    pass

from django.shortcuts import render_to_response
from charter.models import Chart# , ChartDataSet, DataRow

def home(request):
    return render_to_response('home.html')

def signin(request):
    # likely handled by appengine, but might require a callback?
    pass

def manual_data_import(request):
    if request.method == "POST":
        pass
    pass

def bulk_data_import(request):
    pass

def chart_detail(request):
    pass

def chart_list(request):
    pass

def get_chart_resource(request):
    pass

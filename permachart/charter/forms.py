from collections import defaultdict
from django.http import QueryDict
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from charter.models import Chart, ChartDataSet, DataRow
from charter.form_utils import BaseFormSet

class ChartForm(djangoforms.ModelForm):
    class Meta:
        model = Chart
        exclude = ('data', 'user', 'hash','counter',)

class DataSetForm(djangoforms.ModelForm):
    class Meta:
        model = ChartDataSet
        exclude = ('previous_version',)
    
    def __init__(self, *args, **kwargs):
        foo = kwargs['instance'].data_rows
        super(DataSetForm, self).__init__(*args, **kwargs)

class DataRowForm(djangoforms.ModelForm):
    class Meta:
        model = DataRow

class DataRowFormSet(BaseFormSet):
    base_form = DataRowForm

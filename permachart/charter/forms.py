from google.appengine.ext.db import djangoforms
from charter.models import Chart, ChartDataSet

class ChartForm(djangoforms.ModelForm):
    class Meta:
        model = Chart
        exclude = ('data', 'user', 'hash',)

class DataSetForm(djangoforms.ModelForm):
    class Meta:
        model = ChartDataSet
        exclude = ('previous_version',)

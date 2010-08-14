from google.appengine.ext.db import djangoforms
from charter.models import Chart

class ChartForm(djangoforms.ModelForm):
    class Meta:
        model = Chart
        exclude = ('data', 'user', 'hash',)

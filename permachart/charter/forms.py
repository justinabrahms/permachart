from collections import defaultdict
from django.http import QueryDict
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from charter.models import Chart, ChartDataSet, DataRow

class ChartForm(djangoforms.ModelForm):
    class Meta:
        model = Chart
        exclude = ('data', 'user', 'hash',)

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

class DataRowFormSet(object):
    base_form = DataRowForm

    def __init__(self, data=None, instances=None):
        """
        Testing Concerns:
         - deleting an item
         - adding an item
         - altering the key
         - altering the value
        """
        self.forms = []
        for i, obj in enumerate(instances):
            if isinstance(obj, db.Key):
                # fetch keys for validation
                # FIXME: Can probably do a bulk get
                obj = db.get(obj)
            if data:
                self.forms.append(
                    self.base_form(
                        instance=obj,
                        data=data,
                        prefix="%i" % i,
                    )
                )

            else:
                self.forms.append(
                    self.base_form(
                        instance=obj,
                        prefix="%i" % i,
                    )
                )
    
    def is_valid(self):
        for dr in self.forms:
            if not dr.is_valid():
                return False
        return True

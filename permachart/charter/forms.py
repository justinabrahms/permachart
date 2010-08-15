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

    def __init__(self, data=None, instances=None, extra_forms=2):
        """
        Testing Concerns:
         - deleting an item
         - adding an item
         - altering the key
         - altering the value
        """
        self.forms = []
        instances = instances or []
        for i, obj in enumerate(instances):
            if isinstance(obj, db.Key):
                # fetch keys for validation
                # FIXME: Can probably do a bulk get
                obj = db.get(obj)
            if data:
                base_form = self.base_form(
                    instance=obj,
                    data=data,
                    prefix="%i" % i,
                )
            else:
                base_form = self.base_form(
                    instance=obj,
                    prefix="%i" % i,
                )
            self.forms.append(base_form)

        offset = len(instances)
        for i in range(extra_forms):
            if data:
                base_form = self.base_form(
                    data=data,
                    prefix="%i" % (offset+i),
                )
                self.forms.append(base_form)
            else:
                base_form = self.base_form(
                    prefix="%i" % (offset+i),
                )
                self.forms.append(base_form)
    
    def is_valid(self):
        for dr in self.forms:
            if not dr.is_valid():
                return False
        return True

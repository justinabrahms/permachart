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
        formset_dict = defaultdict(QueryDict)
        self.forms = []
            
        if data:
            if not hasattr(data, '__iter__'):
                raise KeyError("data attribute must be an iterable.")
            if len(instances) == len(data):
                raise KeyError("data and instances iterables must be the same length")

            data._mutable = True
            for key, val in dict(data).iteritems():
                data.pop(key)
                num, key = key.split('-', 1)
                if num in formset_dict:
                    formset_dict[num].update({key:val})
                else:
                    formset_dict[num] = QueryDict({key:val})

            # FIXME: Validate that data and instances will always return in the same order
            for i, obj in enumerate(instances):
                if isinstance(obj, db.Key):
                    # fetch keys for validation
                    # FIXME: Can probably do a bulk get
                    obj = db.get(obj)
                data = formset_dict[str(i)]

                self.forms.append(
                    self.base_form(
                        instance=obj,
                        data=data,
                        prefix="%i" % i,
                    )
                )
        else:
            for i, obj in enumerate(instances):
                if isinstance(obj, db.Key):
                    # fetch keys for validation
                    # FIXME: Can probably do a bulk get
                    obj = db.get(obj)
                try:
                    data = formset_dict[i]
                except IndexError:
                    data = None

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

import hashlib
from google.appengine.ext import db

from charter.utils import _cht, get_graph

CHART_CHOICES = ('pie','bar','line',)

class ChartDataSet(db.Model):
    version = db.IntegerProperty(required=True)
    previous_version = db.SelfReferenceProperty()
    data_rows = db.ListProperty(db.Key)
    
class DataRow(db.Model):
    data_key = db.StringProperty(required=True)
    data_value = db.StringProperty(required=True)

class Chart(db.Model):
    name = db.StringProperty(required=True)
    hash = db.StringProperty()
    chart_type = db.StringProperty(required=True, choices=CHART_CHOICES)
    user = db.UserProperty()
    data = db.ReferenceProperty(ChartDataSet)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.chart_type)

    def get_hash(self):
        # FIXME: Bad hashing key/method.
        return hashlib.md5(self.name).hexdigest()

    def put(self, *args, **kwargs):
        self.hash = self.get_hash()
        super(Chart, self).put(*args, **kwargs)
    
    def small_chart(self):
        url, graph = get_graph(self.data, _cht[self.chart_type], 180, 144, 2)
        return graph

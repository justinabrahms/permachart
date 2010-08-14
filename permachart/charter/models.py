from google.appengine.ext import db


class ChartDataSet(db.Model):
    version = db.IntegerProperty(required=True)
    previous_version = db.SelfReferenceProperty()
    data_rows = db.ListProperty(db.Key)
    
class DataRow(db.Model):
    data_key = db.StringProperty(required=True)
    data_value = db.StringProperty(required=True)

class Chart(db.Model):
    name = db.StringProperty(required=True)
    chart_type = db.StringProperty(required=True)
    user = db.UserProperty()
    data = db.ReferenceProperty(ChartDataSet)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.chart_type)

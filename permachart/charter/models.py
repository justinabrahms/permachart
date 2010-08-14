from google.appengine.ext import db

class Chart(db.Model):
    name = db.StringProperty(required=True)
    chart_type = db.StringProperty(required=True)
    user = db.UserProperty()
    data = db.Key(ChartDataSet)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.chart_type)

class ChartDataSet(db.Model):
    chart = db.Key(required=True)
    version = db.IntegerProperty(required=True)
    previous_version = db.SelfReferenceProperty()
    data_rows = db.ListProperty(db.Key)
    
class DataRow(db.Model):
    key = db.StringProperty(required=True)
    value = db.StringProperty(required=True)

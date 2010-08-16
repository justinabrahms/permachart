import hashlib
from google.appengine.ext import db
from google.appengine.api import memcache
from charter.utils import _cht, get_graph, pretty_encode

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
    chart_type = db.StringProperty(required=True, choices=CHART_CHOICES)
    user = db.UserProperty()
    data = db.ReferenceProperty(ChartDataSet)
    counter = db.IntegerProperty(default=0)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.chart_type)

    def get_hash(self):
        return pretty_encode(self.key().id())

    def small_chart(self):
        try:
            url, graph = get_graph(self.data, _cht[self.chart_type], 180, 144, 2)
        except ValueError:
            graph = ''
        return graph

    def small_chart_url(self):
         try:
            url, graph = get_graph(self.data, _cht[self.chart_type], 180, 144, 2)
        except ValueError:
            url = ''
        return url

    def incrementCounter(self, update_interval=10):
      """
      Increments a memcached counter. Snippet was pulled from the
      appengine cookbook at:

        http://appengine-cookbook.appspot.com/recipe/high-concurrency-counters-without-sharding/
      
      Args:
        key: The key of a datastore entity that contains the counter.
        update_interval: Minimum interval between updates.
      """
      lock_key = "counter_lock:%s" % (self.get_hash(),)
      count_key = "counter_value:%s" % (self.get_hash(),)
      if memcache.add(lock_key, None, time=update_interval):
        # Time to update the DB
        count = int(memcache.get(count_key) or 0) + 1
        def tx():
          self.counter += count
          self.put()
        db.run_in_transaction(tx)
        memcache.delete(count_key)
      else:
        # Just update memcache
        memcache.incr(count_key, initial_value=0)

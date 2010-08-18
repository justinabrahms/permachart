import hashlib
from google.appengine.ext import db
from google.appengine.api import memcache
from django.core.urlresolvers import reverse

from charter.utils import _cht, get_graph, pretty_encode, pretty_decode

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
    has_data = db.BooleanProperty(default=False)
    counter = db.IntegerProperty(default=0)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.chart_type)

    def get_hash(self):
        return pretty_encode(self.key().id())

    def small_chart(self, data=None):
        if not data:
            data = self.data
        try:
            return get_graph(data, _cht[self.chart_type], 180, 144, 2)
        except ValueError:
            return ''

    def small_chart_graph(self, data=None):
        return self.small_chart(data=data)[1]

    def small_chart_url(self, data=None):
        return self.small_chart(data=data)[0]

    @classmethod
    def get_by_hash(cls, hash):
        return cls.get_by_id(pretty_decode(hash))

    def get_absolute_url(self):
        if self.data.version == 1:
            return reverse('chart-detail', args=(self.get_hash(),))
        else:
            return reverse('chart-detail-version', args=(self.get_hash(), str(self.data.key())))

    def get_chart_url(self, recent=False, data=None):
        if not data:
            data = self.data
        if self.data.version == 1 or recent:
            return reverse('chart-resource', args=(self.get_hash(),))
        else:
            return reverse('chart-resource-version', args=(self.get_hash(), str(data.key())))

    def get_recent_chart_url(self):
        return self.get_chart_url(recent=True)

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

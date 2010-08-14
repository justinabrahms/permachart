from charter.models import DataRow

from urllib import quote
from urlparse import urlunparse


_cht = dict({
    'pie': 'p3',
})

def get_graph_url(dataset,cht='p3'):
    api = "http://chart.apis.google.com/chart?"
    data = dict()
    data['cht'] = cht
    data['chs'] = '600x480'
    values = []
    chl = []
    chd = []
    summation = 0
    for data_item in dataset.data_rows:
        row = DataRow.get(data_item)
        values.append(float(row.data_value))
        chl.append(row.data_key)
    for value in values:
        summation += value
    for value in values:
        chd.append(str(value/summation))
    data['chd'] = 't:' + ','.join(chd)
    data['chl'] = '|'.join(chl)
    query = '&'.join([k+'='+quote(str(v)) for (k,v) in data.items()])
    return urlunparse((
        'http', 
        'chart.apis.google.com',
        '/chart',
        '',
        query,
        ''
    ))

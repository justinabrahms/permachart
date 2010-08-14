from urlparse import urlunparse

_cht = dict({
    'pie': 'p',
})

def get_graph_url(dataset,cht='p3'):
    api = "http://chart.apis.google.com/chart?"
    data = dict()
    data['cht'] = cht
    data['chs'] = '600x480'
    chd = []
    chl = []
    for data_item in dataset.data_rows:
        chd.append(data_item.data_value)
        chl.append(data_item.data_key)
    data['chd'] = 't:' + ','.join(chd)
    data['chl'] = '|'.join(chl)
    query = '&'.join([k+'='+urllib.quote(str(v)) for (k,v) in data.items()])
    return urlunparse((
        'http', 
        'chart.apis.google.com',
        '/chart',
        '',
        query,
        ''
    ))
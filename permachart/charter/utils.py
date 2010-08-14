from charter.models import DataRow
import pygooglechart

from urllib import quote
from urlparse import urlunparse


_cht = dict({
    'pie': 'p3',
    'pie2d': 'p',
})

def get_graph_url(dataset,cht='p3'):
    data = dict({})
    data['cht'] = cht
    data['chs'] = '600x480'
    chl = []
    chd = []
    for data_item in dataset.data_rows:
        row = DataRow.get(data_item)
        chl.append(row.data_key)
        chd.append(float(row.data_value))
    if cht == 'p3':
        G = pygooglechart.PieChart3D(600,480)
        G.set_pie_labels(chl)
    if cht == 'p':
        G = pygooglechart.PieChart2D(600,480)
        G.set_pie_labels(chl)
    G.add_data(chd)
    return G.get_url(), G
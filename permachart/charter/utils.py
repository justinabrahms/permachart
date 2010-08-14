from charter.models import DataRow
import pygooglechart

from urllib import quote
from urlparse import urlunparse

ALPHABET="23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"

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

def pretty_encode(num, alphabet=ALPHABET):
    """Encode a number in Base X

    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

def pretty_decode(string, alphabet=ALPHABET):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num
>>>>>>> 48289d9ad8831515ea3aa7d5fe739745535a7a4d

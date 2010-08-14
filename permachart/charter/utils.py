from charter.models import DataRow

from urllib import quote
from urlparse import urlunparse

ALPHABET="23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"

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

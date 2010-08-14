from charter.models import DataRow
import pygooglechart

from urllib import quote
from urlparse import urlunparse

ALPHABET="23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"

_cht = dict({
    'pie': 'p3',
    'pie2d': 'p',
    'bar': 'bvg',
    'line': 'lc',
})

WIDTH = 600
HEIGHT = 480
SPACE_TO_BAR = .6

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
    maxim = -1
    minim = 5000
    for ch in chd:
        if ch > maxim:
            maxim = int(ch)
        if ch < minim:
            minim = int(ch)
            
    yrange = (minim, maxim)
    y_steps = 6
    y_step = (yrange[1] - yrange[0]) / y_steps
    y_axis = []
    for x in range(y_steps):
        y_axis.append((x * y_step) + yrange[0])
    y_axis.append(yrange[1])

    if cht == 'p3':
        G = pygooglechart.PieChart3D(WIDTH,HEIGHT)
        G.set_pie_labels(chl)
    if cht == 'p':
        G = pygooglechart.PieChart2D(WIDTH,HEIGHT)
        G.set_pie_labels(chl)
    if cht == 'bvg':
        G = pygooglechart.GroupedVerticalBarChart(WIDTH, HEIGHT, y_range=yrange)
        bars = WIDTH / len(chd)
        G.set_axis_labels(pygooglechart.Axis.LEFT, y_axis)
        G.set_axis_labels(pygooglechart.Axis.BOTTOM, chl)
        G.set_bar_width(int(bars * SPACE_TO_BAR))
        G.set_bar_spacing(int(bars * (.9 - SPACE_TO_BAR)))
        G.set_group_spacing(int(bars * (.9 - SPACE_TO_BAR)))
    if cht == 'lc':
        G = pygooglechart.SimpleLineChart(WIDTH, HEIGHT, y_range=yrange)
        G.set_axis_labels(pygooglechart.Axis.LEFT, y_axis)
        G.set_axis_labels(pygooglechart.Axis.BOTTOM, chl)
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

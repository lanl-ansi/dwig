import os, sys, json, bqpjson

from collections import namedtuple

class DWIGException(Exception):
    pass

Range = namedtuple('Range', ['lb', 'ub'])

default_cell_size = 8
default_site_range = Range(-2.0, 2.0)
default_coupler_range = Range(-1.0, 1.0)

# prints a line to standard error
def print_err(data):
    sys.stderr.write(str(data)+'\n')

json_dumps_kwargs = {
    'sort_keys':True,
    'indent':2,
    'separators':(',', ': ')
}

bqpjson_version = '1.0.0'

def validate_bqp_data(data):
    bqpjson.validate(data)
    return True

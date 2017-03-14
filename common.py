import os, sys, json, bqpjson

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

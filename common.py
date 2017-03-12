import os, sys, json, bqpjson

# prints a line to standard error
def print_err(data):
    sys.stderr.write(str(data)+'\n')

json_dumps_kwargs = {
    'sort_keys':True,
    'indent':2,
    'separators':(',', ': ')
}

bqpjson_version = '0.1.0'

def validate_bqp_data(data):
    try:
        bqpjson.validate(data)
    except ValidationError as e:
        data_string = json.dumps(data, **json_dumps_kwargs)
        print_err(data_string)
        raise e
    return True
    
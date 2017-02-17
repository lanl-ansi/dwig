import os, sys, json

# prints a line to standard error
def print_err(data):
    sys.stderr.write(str(data)+'\n')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bqp-schema.json')) as file:
    qbp_schema = json.load(file)

json_dumps_kwargs = {
    'sort_keys':True,
    'indent':2,
    'separators':(',', ': ')
}

# this is slow in python 2
from jsonschema import validate, ValidationError

def validate_bqp_data(data):
    # skip due to slow loading in python 2
#    return True

    try:
        validate(data, qbp_schema)
    except ValidationError as e:
        data_string = json.dumps(data, **json_dumps_kwargs)
        print_err(data_string)
        raise e
    return True
    
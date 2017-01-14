import os, sys, json
from jsonschema import validate, ValidationError

# prints a line to standard error
def print_err(data):
    sys.stderr.write(str(data)+'\n')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bqp-schema.json')) as file:
    qbp_schema = json.load(file)

def validate_bqp_data(data):
    try:
        validate(data, qbp_schema)
    except ValidationError as e:
        data_string = json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))
        print_err(data_string)
        raise e
    return True
    
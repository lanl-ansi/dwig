import sys, os, json

if (sys.version_info > (3, 0)):
    from io import StringIO
else:
    from cStringIO import StringIO

sys.path.append('.')

import dwig

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


bqp_files = []
for wd, directory, files in os.walk(data_dir):
    for file in files:
        if file.endswith('.json'):
            bqp_files.append(wd+'/'+file)
del wd, directory, files


def json_comp(parser, capfd, ground_truth_file, cli_args):
    with open(os.path.join(data_dir, ground_truth_file)) as file:
        ground_truth = json.load(file)

    json_output = run_dwig_cli(parser, cli_args)
    resout, reserr = capfd.readouterr()

    # The exact value of 'evaluation' may vary across different runs because it
    # depends on the order of iterating over set/dict objects. See how this value
    # is computed in the method 'eval' of QPUAssignment in structure.py file.
    if 'solutions' in ground_truth:
        del ground_truth['solutions'][0]['evaluation']
        del json_output['solutions'][0]['evaluation']

    assert(ground_truth == json_output)


def run_dwig_cli(parser, cli_args):
    output = StringIO()
    dwig.main(parser.parse_args(cli_args), output)
    json_output = json.loads(output.getvalue())
    return json_output

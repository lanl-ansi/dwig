import sys, os, json

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

    output = StringIO()
    dwig.main(parser.parse_args(cli_args), output)

    resout, reserr = capfd.readouterr()

    json_output = json.loads(output.getvalue())

    assert(ground_truth == json_output)

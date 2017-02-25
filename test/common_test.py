import sys, os, json

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

    dwig.main(parser.parse_args(cli_args))

    resout, reserr = capfd.readouterr()

    json_output = json.loads(resout)

    remove_generated(ground_truth)
    remove_generated(json_output)
    assert(ground_truth == json_output)


def remove_generated(data):
    if 'metadata' in data and 'generated' in data['metadata']:
        del data['metadata']['generated']
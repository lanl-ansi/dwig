import sys, os, json

sys.path.append('.')

import dwig


data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def json_comp(parser, capfd, ground_truth_file, cli_args):
    with open(os.path.join(data_dir, ground_truth_file)) as file:
        ground_truth = json.load(file)

    dwig.main(parser.parse_args(cli_args))

    resout, reserr = capfd.readouterr()

    json_output = json.loads(resout)
    assert(ground_truth == json_output)

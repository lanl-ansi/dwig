#!/usr/bin/env python3

import sys, json, argparse

from common import print_err
from common import validate_bqp_data

# converts a bqp-json file to a qubo data file
def main(args):
    try:
        data = json.load(sys.stdin)
    except:
        print_err('unable to parse stdin as a json document')
        quit()
    validate_bqp_data(data)

    if data['variable_domain'] == 'spin':
        print_err('Error: unable to generate qubo data file from stdin, only boolean domains are supported by qubo')
        quit()

    for k,v in data['metadata'].items():
         print('c {} : {}'.format(k,v))

    max_index = max(data['variable_idxs'])+1
    num_diagonals = len(data['linear_terms'])
    num_elements = len(data['quadratic_terms'])

    print('p qubo 0 {} {} {}'.format(max_index, num_diagonals, num_elements))

    print('c linear terms')
    for term in data['linear_terms']:
        print('{} {} {}'.format(term['idx'], term['idx'], term['coeff']))

    print('c quadratic terms')
    for term in data['quadratic_terms']:
        print('{} {} {}'.format(term['idx_1'], term['idx_2'], term['coeff']))


def build_cli_parser():
    parser = argparse.ArgumentParser(description='a command line tool for converting a bqp-json files to a qubo format.  The default input is stdin and the default output is stdout.')
    return parser


if __name__ == '__main__':
    parser = build_cli_parser()
    main(parser.parse_args())
#!/usr/bin/env python

import sys, json, argparse

from common import print_err
from common import validate_bqp_data

# converts a bqp json file to a qubist hamiltonian
def main(args):
    data = json.load(sys.stdin)
    validate_bqp_data(data)

    if data['variable_domain'] == 'boolean':
        print_err('unable to generate qubist hamiltonian from stdin, only spin domains are supported at this time')
        quit()

    sites = len(data['variable_idxs'])
    lines = len(data['linear_terms']) + len(data['quadratic_terms'])

    print('%d %d' % (sites, lines))
    for lt in data['linear_terms']:
        print('%d %d %f' % (lt['idx'], lt['idx'], lt['coeff']))
    for qt in data['quadratic_terms']:
        print('%d %d %f' % (qt['idx_1'], qt['idx_2'], qt['coeff']))


def build_cli_parser():
    parser = argparse.ArgumentParser(description='a command line tool for converting a B-QP json files to a qubist hamiltonians.  The default input is stdin and the default output is stdout.')
    return parser

if __name__ == '__main__':
    parser = build_cli_parser()
    main(parser.parse_args())
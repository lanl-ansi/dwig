#!/usr/bin/env python2

import sys, json, argparse

from common import print_err
from common import validate_bqp_data

# converts a bqp-json file to a qubist hamiltonian
def main(args, data_stream):
    try:
        data = json.load(data_stream)
    except:
        print_err('unable to parse stdin as a json document')
        quit()
    validate_bqp_data(data)

    if data['variable_domain'] == 'boolean':
        print_err('Error: unable to generate qubist hamiltonian from stdin, only spin domains are supported by qubist')
        quit()

    sites = max(data['variable_idxs'])+1
    lines = len(data['linear_terms']) + len(data['quadratic_terms'])

    print('{} {}'.format(sites, lines))
    for lt in data['linear_terms']:
        print('{} {} {}'.format(lt['idx'], lt['idx'], lt['coeff']))
    for qt in data['quadratic_terms']:
        print('{} {} {}'.format(qt['idx_1'], qt['idx_2'], qt['coeff']))


def build_cli_parser():
    parser = argparse.ArgumentParser(description='a command line tool for converting a bqp-json files to a qubist hamiltonians.  The default input is stdin and the default output is stdout.')
    return parser


if __name__ == '__main__':
    parser = build_cli_parser()
    main(parser.parse_args(), sys.stdin)
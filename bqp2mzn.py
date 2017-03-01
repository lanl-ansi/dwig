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
        print('set of int: Domain = {0,1};')
    elif data['variable_domain'] == 'spin':
        print('set of int: Domain = {-1,1};')
    else:
        print_err('Error: unknown variable domain')
        quit()

    print('')
    mzn_var = {}
    for var_idx in data['variable_idxs']:
        mzn_var[var_idx] = 'x{}'.format(var_idx)
        print('var Domain: {};'.format(mzn_var[var_idx]))

    objective_terms = []
    for lt in data['linear_terms']:
        objective_terms.append('{}*{}'.format(lt['coeff'], mzn_var[lt['idx']]))
    for qt in data['quadratic_terms']:
        objective_terms.append('{}*{}*{}'.format(qt['coeff'], mzn_var[qt['idx_1']], mzn_var[qt['idx_2']]))

    print('')
    objective_expr = ' + '.join(objective_terms)
    print('var float: objective = {};'.format(objective_expr))

    print('')
    print('solve minimize objective;'.format(objective_expr))



def build_cli_parser():
    parser = argparse.ArgumentParser(description='a command line tool for converting a bqp-json files to a qubist hamiltonians.  The default input is stdin and the default output is stdout.')
    return parser


if __name__ == '__main__':
    parser = build_cli_parser()
    main(parser.parse_args(), sys.stdin)
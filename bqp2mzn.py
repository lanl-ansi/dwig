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

    print('% id : {}'.format(data['id']))

    if 'description' in data:
        print('% description : {}'.format(data['description']))
    print('% ')

    for k in sorted(data['metadata']):
         print('% {} : {}'.format(k, data['metadata'][k]))

    print('')
    if data['variable_domain'] == 'boolean':
        print('set of int: Domain = {0,1};')
    elif data['variable_domain'] == 'spin':
        print('set of int: Domain = {-1,1};')
    else:
        print_err('Error: unknown variable domain')
        quit()

    print('float: offset = {};'.format(data['offset']))
    print('float: scale = {};'.format(data['scale']))
    # this does not work becuose minizinc requires "array index set must be contiguous range"
    #var_ids_str = [str(var_id) for var_id in data['variable_id']]
    #print('set of int: Vars = {{{}}};'.format(','.join(var_ids_str)))

    print('')
    mzn_var = {}
    for var_id in data['variable_ids']:
        mzn_var[var_id] = 'x{}'.format(var_id)
        print('var Domain: {};'.format(mzn_var[var_id]))

    #print('array[Vars] of var Domain: x;')

    objective_terms = []
    for lt in data['linear_terms']:
        objective_terms.append('{}*{}'.format(lt['coeff'], mzn_var[lt['id']]))
    for qt in data['quadratic_terms']:
        objective_terms.append('{}*{}*{}'.format(qt['coeff'], mzn_var[qt['id_tail']], mzn_var[qt['id_head']]))

    # objective_terms = []
    # for lt in data['linear_terms']:
    #     objective_terms.append('{}*x[{}]'.format(lt['coeff'],lt['id']))
    # for qt in data['quadratic_terms']:
    #     objective_terms.append('{}*x[{}]*x[{}]'.format(qt['coeff'], qt['id_tail'], qt['id_head']))

    print('')
    objective_expr = ' + '.join(objective_terms)
    print('var float: objective = {};'.format(objective_expr))

    print('')
    print('solve minimize objective;'.format(objective_expr))

    print('')
    var_list = []
    for var_id in data['variable_ids']:
        var_list.append(mzn_var[var_id])
    print('output [show(scale*(objective + offset)), " - ", show(objective), " - ", show([{}])];'.format(', '.join(var_list)))

    # print('')
    # print('output [show(objective), " - ", show(x)]')

def build_cli_parser():
    parser = argparse.ArgumentParser(description='a command line tool for converting a bqp-json files to a qubist hamiltonians.  The default input is stdin and the default output is stdout.')
    return parser


if __name__ == '__main__':
    parser = build_cli_parser()
    main(parser.parse_args(), sys.stdin)
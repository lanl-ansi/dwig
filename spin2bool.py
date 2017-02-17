#!/usr/bin/env python

import sys, json, argparse, copy

from common import print_err
from common import validate_bqp_data
from common import json_dumps_kwargs

# converts a B-QP json file from the ising space to the boolean space and vise versa.
def main(args):
    try:
        data = json.load(sys.stdin)
    except:
        print_err('unable to parse stdin as a json document')
        quit()

    output_data = transform(data)

    validate_bqp_data(output_data)
    output_string = json.dumps(output_data, **json_dumps_kwargs)
    print(output_string)


def transform(data):
    validate_bqp_data(data)
    if data['variable_domain'] == 'spin':
        output_data = spin_to_bool(data)
    else:
        output_data = bool_to_spin(data)
    return output_data


def spin_to_bool(ising_data):
    offset = 0
    coefficients = {}

    for v_idx in ising_data['variable_idxs']:
        coefficients[(v_idx, v_idx)] = 0

    for linear_term in ising_data['linear_terms']:
        v_idx = linear_term['idx']
        coeff = linear_term['coeff']
        assert(coeff != 0.0)

        coefficients[(v_idx, v_idx)] = 2*coeff
        offset += -coeff

    for quadratic_term in ising_data['quadratic_terms']:
        v1_idx = quadratic_term['idx_1']
        v2_idx = quadratic_term['idx_2']
        assert(v1_idx != v2_idx)
        if v1_idx > v2_idx:
            v1_idx = quadratic_term['idx_2']
            v2_idx = quadratic_term['idx_1']
        coeff = quadratic_term['coeff']
        assert(coeff != 0)

        if not (v1_idx, v2_idx) in coefficients:
            coefficients[(v1_idx, v2_idx)] = 0

        coefficients[(v1_idx, v2_idx)] = coefficients[(v1_idx, v2_idx)] + 4*coeff
        coefficients[(v1_idx, v1_idx)] = coefficients[(v1_idx, v1_idx)] - 2*coeff
        coefficients[(v2_idx, v2_idx)] = coefficients[(v2_idx, v2_idx)] - 2*coeff
        offset += coeff

    linear_terms = []
    quadratic_terms = []

    for (i,j) in sorted(coefficients.keys()):
        v = coefficients[(i,j)]
        if v != 0.0:
            if i == j:
                linear_terms.append({'idx':i, 'coeff':v})
            else:
                quadratic_terms.append({'idx_1':i, 'idx_2':j, 'coeff':v})

    bool_data = copy.deepcopy(ising_data)
    bool_data['variable_domain'] = 'boolean'
    bool_data['linear_terms'] = linear_terms
    bool_data['quadratic_terms'] = quadratic_terms

    return bool_data


def bool_to_spin(bool_data):
    offset = 0
    coefficients = {}

    for v_idx in bool_data['variable_idxs']:
        coefficients[(v_idx, v_idx)] = 0

    for linear_term in bool_data['linear_terms']:
        v_idx = linear_term['idx']
        coeff = linear_term['coeff']
        assert(coeff != 0.0)

        coefficients[(v_idx, v_idx)] = coeff/2
        offset += linear_term['coeff']/2

    for quadratic_term in bool_data['quadratic_terms']:
        v1_idx = quadratic_term['idx_1']
        v2_idx = quadratic_term['idx_2']
        assert(v1_idx != v2_idx)
        if v1_idx > v2_idx:
            v1_idx = quadratic_term['idx_2']
            v2_idx = quadratic_term['idx_1']
        coeff = quadratic_term['coeff']
        assert(coeff != 0)

        if not (v1_idx, v2_idx) in coefficients:
            coefficients[(v1_idx, v2_idx)] = 0

        coefficients[(v1_idx, v2_idx)] = coefficients[(v1_idx, v2_idx)] + coeff/4
        coefficients[(v1_idx, v1_idx)] = coefficients[(v1_idx, v1_idx)] + coeff/4
        coefficients[(v2_idx, v2_idx)] = coefficients[(v2_idx, v2_idx)] + coeff/4
        offset += coeff/4

    linear_terms = []
    quadratic_terms = []

    for (i,j) in sorted(coefficients.keys()):
        v = coefficients[(i,j)]
        if v != 0.0:
            if i == j:
                linear_terms.append({'idx':i, 'coeff':v})
            else:
                quadratic_terms.append({'idx_1':i, 'idx_2':j, 'coeff':v})

    ising_data = copy.deepcopy(bool_data)
    ising_data['variable_domain'] = 'spin'
    ising_data['linear_terms'] = linear_terms
    ising_data['quadratic_terms'] = quadratic_terms

    return ising_data


def build_cli_parser():
    parser = argparse.ArgumentParser(description='a command line tool for converting a B-QP json files from ising to boolean variables and back.  The default input is stdin and the default output is stdout.')
    return parser

if __name__ == '__main__':
    parser = build_cli_parser()
    main(parser.parse_args())
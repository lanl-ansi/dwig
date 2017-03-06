#!/usr/bin/env python2

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
    offset = ising_data['offset']
    coefficients = {}

    for v_id in ising_data['variable_ids']:
        coefficients[(v_id, v_id)] = 0.0

    for linear_term in ising_data['linear_terms']:
        v_id = linear_term['id']
        coeff = linear_term['coeff']
        assert(coeff != 0.0)

        coefficients[(v_id, v_id)] = 2.0*coeff
        offset += -coeff

    for quadratic_term in ising_data['quadratic_terms']:
        v_id1 = quadratic_term['id_tail']
        v_id2 = quadratic_term['id_head']
        assert(v_id1 != v_id2)
        # if v_id1 > v_id2:
        #     v_id1 = quadratic_term['id_head']
        #     v_id2 = quadratic_term['id_tail']
        coeff = quadratic_term['coeff']
        assert(coeff != 0.0)

        if not (v_id1, v_id2) in coefficients:
            coefficients[(v_id1, v_id2)] = 0.0

        coefficients[(v_id1, v_id2)] = coefficients[(v_id1, v_id2)] + 4.0*coeff
        coefficients[(v_id1, v_id1)] = coefficients[(v_id1, v_id1)] - 2.0*coeff
        coefficients[(v_id2, v_id2)] = coefficients[(v_id2, v_id2)] - 2.0*coeff
        offset += coeff

    linear_terms = []
    quadratic_terms = []

    for (i,j) in sorted(coefficients.keys()):
        v = coefficients[(i,j)]
        if v != 0.0:
            if i == j:
                linear_terms.append({'id':i, 'coeff':v})
            else:
                quadratic_terms.append({'id_tail':i, 'id_head':j, 'coeff':v})

    bool_data = copy.deepcopy(ising_data)
    bool_data['variable_domain'] = 'boolean'
    bool_data['offset'] = offset
    bool_data['linear_terms'] = linear_terms
    bool_data['quadratic_terms'] = quadratic_terms

    if 'solutions' in bool_data:
        for solution in bool_data['solutions']:
            for assign in solution['assignment']:
                if assign['value'] == -1:
                    assign['value'] = 0

    return bool_data


def bool_to_spin(bool_data):
    offset = bool_data['offset']
    coefficients = {}

    for v_id in bool_data['variable_ids']:
        coefficients[(v_id, v_id)] = 0.0

    for linear_term in bool_data['linear_terms']:
        v_id = linear_term['id']
        coeff = linear_term['coeff']
        assert(coeff != 0.0)

        coefficients[(v_id, v_id)] = coeff/2.0
        offset += linear_term['coeff']/2.0

    for quadratic_term in bool_data['quadratic_terms']:
        v_id1 = quadratic_term['id_tail']
        v_id2 = quadratic_term['id_head']
        assert(v_id1 != v_id2)
        # if v_id1 > v_id2:
        #     v_id1 = quadratic_term['id_head']
        #     v_id2 = quadratic_term['id_tail']
        coeff = quadratic_term['coeff']
        assert(coeff != 0.0)

        if not (v_id1, v_id2) in coefficients:
            coefficients[(v_id1, v_id2)] = 0.0

        coefficients[(v_id1, v_id2)] = coefficients[(v_id1, v_id2)] + coeff/4.0
        coefficients[(v_id1, v_id1)] = coefficients[(v_id1, v_id1)] + coeff/4.0
        coefficients[(v_id2, v_id2)] = coefficients[(v_id2, v_id2)] + coeff/4.0
        offset += coeff/4.0

    linear_terms = []
    quadratic_terms = []

    for (i,j) in sorted(coefficients.keys()):
        v = coefficients[(i,j)]
        if v != 0.0:
            if i == j:
                linear_terms.append({'id':i, 'coeff':v})
            else:
                quadratic_terms.append({'id_tail':i, 'id_head':j, 'coeff':v})

    ising_data = copy.deepcopy(bool_data)
    ising_data['variable_domain'] = 'spin'
    ising_data['offset'] = offset
    ising_data['linear_terms'] = linear_terms
    ising_data['quadratic_terms'] = quadratic_terms

    if 'solutions' in ising_data:
        for solution in ising_data['solutions']:
            for assign in solution['assignment']:
                if assign['value'] == 0:
                    assign['value'] = -1

    return ising_data


def build_cli_parser():
    parser = argparse.ArgumentParser(description='a command line tool for converting a B-QP json files from ising to boolean variables and back.  The default input is stdin and the default output is stdout.')
    return parser

if __name__ == '__main__':
    parser = build_cli_parser()
    main(parser.parse_args())
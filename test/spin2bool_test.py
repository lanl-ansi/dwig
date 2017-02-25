import sys, os, pytest, json

sys.path.append('.')
import spin2bool

from common_test import bqp_files

eq_tol = 1e-9

@pytest.mark.parametrize('bqp_file', bqp_files)
def test_spin2bool(bqp_file):
    #print(bqp_file)

    with open(bqp_file) as file:
        data_0 = json.load(file)

    data_1 = spin2bool.transform(data_0)
    data_2 = spin2bool.transform(data_1)

    #print(json.dumps(data_2))
    #print('')

    # These tests are required to get around numerical precision issues in floating point arithmetic
    assert(abs(data_0['offset'] - data_2['offset']) < eq_tol)

    for i in range(len(data_0['linear_terms'])):
        assert(abs(data_0['linear_terms'][i]['coeff'] - data_2['linear_terms'][i]['coeff']) < eq_tol)

    for i in range(len(data_0['quadratic_terms'])):
        assert(abs(data_0['quadratic_terms'][i]['coeff'] - data_2['quadratic_terms'][i]['coeff']) < eq_tol)

    for key in ['offset', 'linear_terms', 'quadratic_terms']:
        for data in [data_0, data_2]:
            del data[key]

    assert(data_0 == data_2)

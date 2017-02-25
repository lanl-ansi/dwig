import sys, os, pytest, json

sys.path.append('.')
import bqp2qh

from common_test import bqp_files

@pytest.mark.parametrize('bqp_file', bqp_files)
def test_bqp2qh(bqp_file, capsys):

    with open(bqp_file.replace('.json', '.qh'), 'r') as file:
        base = file.read()

    with open(bqp_file, 'r') as file:
        bqp2qh.main(None, file)

    out, err = capsys.readouterr()

    assert(out.strip() == base.strip())

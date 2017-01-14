import random

from common import print_err

from structure import QPUConfiguration

# Generators take an instance of ChimeraQPU (qpu) and a generate a random problem and return the data as a QPUConfiguration object

# specification provided in https://arxiv.org/abs/1508.05087
def generate_ran(qpu, steps = 1, feild = False):
    assert(isinstance(steps, int))
    assert(steps >= 1)

    choices = range(-steps, 0) + range(1, steps+1)

    fields = {}
    if feild:
        fields = {site : random.choice(choices) for site in qpu.sites}
    couplings = {coupler : random.choice(choices) for coupler in qpu.couplers}
    return QPUConfiguration(qpu, fields, couplings)


def generate_clq(qpu):
    # stub for max clique case generation
    return QPUConfiguration(qpu, {}, {})


def generate_flc(qpu):
    # stub for frustrated loop case generation
    return QPUConfiguration(qpu, {}, {})


def generate_wscn(qpu):
    # stub for weak-strong cluster network case generation
    return QPUConfiguration(qpu, {}, {})


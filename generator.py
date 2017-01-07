import random

from structure import QPUConfiguration

# Generators take an instance of ChimeraQPU (qpu) and a generate a random problem and return the data as a QPUConfiguration object

def generate_ran(qpu, steps = 1):
    couplings = {coupler : -1.0 if random.random() <= 0.5 else 1.0 for coupler in qpu.couplers}
    return QPUConfiguration(qpu, {}, couplings)


def generate_clq(qpu):
    # stub for max clique case generation
    return QPUConfiguration(qpu, {}, {})


def generate_flc(qpu):
    # stub for frustrated loop case generation
    return QPUConfiguration(qpu, {}, {})


def generate_wscn(qpu):
    # stub for weak-strong cluster network case generation
    return QPUConfiguration(qpu, {}, {})


import random, math

from common import print_err

from structure import QPUConfiguration

# Generators take an instance of ChimeraQPU (qpu) and a generate a random problem and return the data as a QPUConfiguration object

# specification provided in https://arxiv.org/abs/1508.05087
def generate_ran(qpu, steps = 1, feild = False):
    assert(isinstance(steps, int))
    assert(steps >= 1)

    choices = range(-steps, 0) + range(1, steps+1)
    choices = [float(x) for x in choices]

    fields = {}
    if feild:
        fields = {site : random.choice(choices) for site in sorted(qpu.sites)}
    couplings = {coupler : random.choice(choices) for coupler in sorted(qpu.couplers)}
    return QPUConfiguration(qpu, fields, couplings)


def generate_clq(qpu):
    # stub for max clique case generation
    return QPUConfiguration(qpu, {}, {})


def generate_flc(qpu):
    # stub for frustrated loop case generation
    return QPUConfiguration(qpu, {}, {})


def generate_wscn(qpu, weak_field, strong_field):
    # stub for weak-strong cluster network case generation
    assert(qpu.chimera_degree >= 6)
    assert(qpu.chimera_degree % 3 == 0)

    c_row_offset = 1
    c_col_offset = 1

    fields, couplings = _build_wscb(qpu, weak_field, strong_field, c_row_offset, c_col_offset)

    return QPUConfiguration(qpu, fields, couplings)


def _build_wscb(qpu, weak_field, strong_field, c_row_offset, c_col_offset):
    fields = {} 
    couplings = {}

    cro = c_row_offset
    cco = c_col_offset
    wscs = [
        (qpu.chimera_cell(cro+1, cco+0), qpu.chimera_cell(cro+1, cco+1)),
        (qpu.chimera_cell(cro+0, cco+2), qpu.chimera_cell(cro+1, cco+2)),
        (qpu.chimera_cell(cro+2, cco+3), qpu.chimera_cell(cro+1, cco+3)),
        (qpu.chimera_cell(cro+0, cco+4), qpu.chimera_cell(cro+1, cco+4)),

        (qpu.chimera_cell(cro+2, cco+2), qpu.chimera_cell(cro+2, cco+1)),
        (qpu.chimera_cell(cro+2, cco+5), qpu.chimera_cell(cro+2, cco+4)),
        
        (qpu.chimera_cell(cro+3, cco+0), qpu.chimera_cell(cro+3, cco+1)),
        (qpu.chimera_cell(cro+3, cco+3), qpu.chimera_cell(cro+3, cco+4)),

        (qpu.chimera_cell(cro+4, cco+0), qpu.chimera_cell(cro+4, cco+1)),
        (qpu.chimera_cell(cro+3, cco+2), qpu.chimera_cell(cro+4, cco+2)),
        (qpu.chimera_cell(cro+5, cco+3), qpu.chimera_cell(cro+4, cco+3)),
        (qpu.chimera_cell(cro+5, cco+4), qpu.chimera_cell(cro+4, cco+4)),
    ]

    strong_cells = sorted(set([swc[1] for swc in wscs]))
    #print(strong_cells)

    for (weak_cell, strong_cell) in wscs:
        wsc_fields, wsc_couplings = _build_wsc(qpu, weak_field, strong_field, weak_cell, strong_cell)
        fields.update(wsc_fields)
        couplings.update(wsc_couplings)

    choices = [-1, 1]

    for i, sc_1 in enumerate(strong_cells):
        for sc_2 in [strong_cells[j] for j in range(i+1, len(strong_cells))]:
            coupling = random.choice(choices)
            #print(sc_1, sc_2, coupling)
            sites_1 = qpu.chimera_cell_sites[sc_1]
            sites_2 = qpu.chimera_cell_sites[sc_2]
            
            #print(sites_1)
            #print(sites_2)

            for (i,j) in qpu.couplers:
                if (i in sites_1 and j in sites_2) or (j in sites_1 and j in sites_2):
                    couplings[(i,j)] = coupling

    return fields, couplings


def _build_wsc(qpu, weak_field, strong_field, c_cell_weak, c_cell_strong):
    fields = {} 
    couplings = {}

    weak_sites = qpu.chimera_cell_sites[c_cell_weak]
    strong_sites = qpu.chimera_cell_sites[c_cell_strong]

    for site in weak_sites:
        fields[site] = weak_field
    for site in strong_sites:
        fields[site] = strong_field

    for (i,j) in qpu.couplers:
        if (i in weak_sites or i in strong_sites) and (j in weak_sites or j in strong_sites):
            couplings[(i,j)] = 1

    return fields, couplings



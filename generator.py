import random, math

from collections import namedtuple

from common import print_err

from structure import QPUConfiguration
from structure import ChimeraCoordinate

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


def generate_fl(qpu):
    # stub for frustrated loop case generation
    return QPUConfiguration(qpu, {}, {})


def generate_wscn(qpu, weak_field, strong_field):
    '''This function builds a weak-strong cluster network as described by,
    https://arxiv.org/abs/1512.02206.  The function assumes that the chimera
    degree of the QPU is a square multiple of 3 that is greater than 5.  As 
    this a necessary condition for building a weak-strong cluster network.

    The function begins by placing a core set of weak-strong cluster 
    blocks, which can be replicated at regular intervals of three chimera 
    cells in the x and y axis.  Second, it adds in the remaining weak-strong 
    clusters which cannot be captured by the repeated sub-structure.  With all 
    of the weak-strong clusters in place, it finished by linking the strong 
    clusters together.
    '''
    assert(qpu.chimera_degree_view >= 6)
    assert(qpu.chimera_degree_view % 3 == 0)

    c_row_offset = 1
    c_col_offset = 1

    fields = {} 
    couplings = {}

    strong_cultsers = []

    steps = qpu.chimera_degree_view/3 - 1

    wscbs = []

    for step_row in range(steps):
        for step_column in range(steps):
            wscbs.append((1 + 3*(step_row), 1+3*(step_column)))

    for c_row_offset, c_col_offset in wscbs:
        wscb_fields, wscb_couplings, wscb_strong_cultsers = _build_wscb(qpu, weak_field, strong_field, c_row_offset, c_col_offset)
        strong_cultsers.extend(wscb_strong_cultsers)
        _update_fc(fields, couplings, wscb_fields, wscb_couplings, strict = False)

    wscbc_fields, wscbc_couplings, wscbc_strong_cultsers = _build_wscbc(qpu, weak_field, strong_field, qpu.chimera_degree_view)
    strong_cultsers.extend(wscbc_strong_cultsers)
    _update_fc(fields, couplings, wscbc_fields, wscbc_couplings)

    scl_fields, scl_couplings = _build_scl(qpu, strong_cultsers)
    _update_fc(fields, couplings, scl_fields, scl_couplings)

    return QPUConfiguration(qpu, fields, couplings)


WeakStrongCluster = namedtuple('WeakStrongCluster', ['weak', 'strong'])

def _build_wscbc(qpu, weak_field, strong_field, chimera_degree_view):
    '''This function adds the parts of the of weak-strong cluster network which
    are not covered by the weak-strong cluster blocks. This function must 
    consider the complete weak-strong cluster network because the semantics 
    vary based on the overlap of the weak-strong cluster blocks.  There are 
    three primary cases: (1) corners of the cluster network; (2) along the 
    boarder of the cluster network; and (3) on the interior of cluster network.
    '''
    fields = {} 
    couplings = {}

    steps = qpu.chimera_degree_view/3

    strong_cultsers = []
    for step_row in range(steps):
        for step_column in range(steps):
            strong_cultsers.append(ChimeraCoordinate(2 + 3*(step_row), 2 + 3*(step_column)))

    #print(strong_cultsers)

    # this works because we assume a square chimera grid
    min_row_col = min([min(sc.row, sc.col) for sc in strong_cultsers])
    max_row_col = max([max(sc.row, sc.col) for sc in strong_cultsers])

    #print(min_row_col, max_row_col)

    ws_cluters = []
    s_clusters = []

    for sc in strong_cultsers:
        # Corner cases
        if sc.row == min_row_col and sc.col == min_row_col:
            wc_1 = ChimeraCoordinate(sc.row-1, sc.col)
            wc_2 = ChimeraCoordinate(sc.row, sc.col-1)
            wc = _select_weak_cluster(qpu, sc, wc_1, wc_2)
            ws_cluters.append(WeakStrongCluster(wc, sc))
        elif sc.row == min_row_col and sc.col == max_row_col:
            wc_1 = ChimeraCoordinate(sc.row-1, sc.col)
            wc_2 = ChimeraCoordinate(sc.row, sc.col+1)
            wc = _select_weak_cluster(qpu, sc, wc_1, wc_2)
            ws_cluters.append(WeakStrongCluster(wc, sc))
        elif sc.row == max_row_col and sc.col == min_row_col:
            wc_1 = ChimeraCoordinate(sc.row+1, sc.col)
            wc_2 = ChimeraCoordinate(sc.row, sc.col-1)
            wc = _select_weak_cluster(qpu, sc, wc_1, wc_2)
            ws_cluters.append(WeakStrongCluster(wc, sc))
        elif sc.row == max_row_col and sc.col == max_row_col:
            wc_1 = ChimeraCoordinate(sc.row+1, sc.col)
            wc_2 = ChimeraCoordinate(sc.row, sc.col-1)
            wc = _select_weak_cluster(qpu, sc, wc_1, wc_2)
            ws_cluters.append(WeakStrongCluster(wc, sc))
        # Row Cases
        elif sc.row == min_row_col and (sc.col != min_row_col or sc.col != max_row_col):
            wc = ChimeraCoordinate(sc.row-1, sc.col)
            ws_cluters.append(WeakStrongCluster(wc, sc))
        elif sc.row == max_row_col and (sc.col != min_row_col or sc.col != max_row_col):
            wc = ChimeraCoordinate(sc.row+1, sc.col)
            ws_cluters.append(WeakStrongCluster(wc, sc))
        # Column Cases
        elif (sc.row != min_row_col or sc.row != max_row_col) and sc.col == min_row_col:
            wc = ChimeraCoordinate(sc.row, sc.col-1)
            ws_cluters.append(WeakStrongCluster(wc, sc))
        elif (sc.row != min_row_col or sc.row != max_row_col) and sc.col == max_row_col:
            wc = ChimeraCoordinate(sc.row, sc.col+1)
            ws_cluters.append(WeakStrongCluster(wc, sc))
        # Interior Case
        elif (sc.row != min_row_col or sc.row != max_row_col) and (sc.col != min_row_col or sc.col != max_row_col):
            wc = ChimeraCoordinate(sc.row, sc.col+1)
            s_clusters.append(sc)
        else:
            assert(False) # Case missing from SWC generator

    for wsc in ws_cluters:
        wsc_fields, wsc_couplings = _build_wsc(qpu, weak_field, strong_field, wsc)
        _update_fc(fields, couplings, wsc_fields, wsc_couplings)

    for sc in s_clusters:
        sc_fields, sc_couplings = _build_sc(qpu, strong_field, sc)
        _update_fc(fields, couplings, sc_fields, sc_couplings)

    return fields, couplings, strong_cultsers


def _select_weak_cluster(qpu, strong_cluster, weak_cluster_1, weak_cluster_2):
    '''There are multiple weak cluster options for the corners of a 
    weak-strong cluster network.  This function is used to select between them.
    '''
    #TODO this could be extended to support some more interesting tie breaking criteria
    return weak_cluster_1


def _build_wscb(qpu, weak_field, strong_field, c_row_offset, c_col_offset):
    '''Given chimera coordinate offsets, builds the repeatable part of and a 
    4x4 weak-string cluster block.  Block corners are left to another method.
    '''
    fields = {} 
    couplings = {}

    cro = c_row_offset
    cco = c_col_offset
    wscs = [
        WeakStrongCluster(ChimeraCoordinate(cro+0, cco+2), ChimeraCoordinate(cro+1, cco+2)),
        WeakStrongCluster(ChimeraCoordinate(cro+2, cco+3), ChimeraCoordinate(cro+1, cco+3)),

        WeakStrongCluster(ChimeraCoordinate(cro+2, cco+2), ChimeraCoordinate(cro+2, cco+1)),
        WeakStrongCluster(ChimeraCoordinate(cro+2, cco+5), ChimeraCoordinate(cro+2, cco+4)),
        
        WeakStrongCluster(ChimeraCoordinate(cro+3, cco+0), ChimeraCoordinate(cro+3, cco+1)),
        WeakStrongCluster(ChimeraCoordinate(cro+3, cco+3), ChimeraCoordinate(cro+3, cco+4)),

        WeakStrongCluster(ChimeraCoordinate(cro+3, cco+2), ChimeraCoordinate(cro+4, cco+2)),
        WeakStrongCluster(ChimeraCoordinate(cro+5, cco+3), ChimeraCoordinate(cro+4, cco+3)),
    ]

    strong_cultsers = []
    for wsc in wscs:
        strong_cultsers.append(wsc.strong)
        wsc_fields, wsc_couplings = _build_wsc(qpu, weak_field, strong_field, wsc)
        _update_fc(fields, couplings, wsc_fields, wsc_couplings)
        #fields.update(wsc_fields)
        #couplings.update(wsc_couplings)

    return fields, couplings, strong_cultsers


def _build_scl(qpu, strong_cultsers):
    '''Given a collection of ChimeraCordinates representing strong clusters, 
    this links these these cells together using random coupler settings
    '''
    fields = {} 
    couplings = {}

    strong_cells = [qpu.chimera_cell(sc) for sc in set(strong_cultsers)]
    strong_cells.sort()

    choices = [-1, 1]

    for i, sc_1 in enumerate(strong_cells):
        for sc_2 in [strong_cells[j] for j in range(i+1, len(strong_cells))]:
            coupling = random.choice(choices)
            #print(sc_1, sc_2, coupling)
            sites_1 = qpu.chimera_cell_sites[sc_1]
            sites_2 = qpu.chimera_cell_sites[sc_2]

            for (i,j) in qpu.couplers:
                if (i in sites_1 and j in sites_2) or (j in sites_1 and j in sites_2):
                    assert(not (i,j) in couplings)
                    couplings[(i,j)] = coupling

    return fields, couplings


def _build_wsc(qpu, weak_field, strong_field, weak_strong_cluster):
    '''Given a WeakStrongCluster, configures the field and couplers of 
    both the weak and strong Chimera cells
    '''
    fields = {} 
    couplings = {}

    weak_chimera_cell = qpu.chimera_cell(weak_strong_cluster.weak)
    strong_chimera_cell = qpu.chimera_cell(weak_strong_cluster.strong)

    weak_sites = qpu.chimera_cell_sites[weak_chimera_cell]
    strong_sites = qpu.chimera_cell_sites[strong_chimera_cell]

    for site in weak_sites:
        fields[site] = weak_field
    for site in strong_sites:
        fields[site] = strong_field

    for (i,j) in qpu.couplers:
        if (i in weak_sites or i in strong_sites) and (j in weak_sites or j in strong_sites):
            couplings[(i,j)] = -1

    return fields, couplings


def _build_sc(qpu, strong_field, strong_cluster):
    '''Given a ChimeraCordinate, configures the field and couplers of a 
    stand alone strong cluster Chimera cell
    '''
    fields = {} 
    couplings = {}

    chimera_cell = qpu.chimera_cell(strong_cluster)

    sites = qpu.chimera_cell_sites[chimera_cell]

    for site in sites:
        fields[site] = strong_field

    for (i,j) in qpu.couplers:
        if (i in sites) and (j in sites):
            couplings[(i,j)] = -1

    return fields, couplings


def _update_fc(fields, couplings, new_fields, new_couplings, strict = True):
    '''Updates the given fields and couplings with given new data.
    By default the function checks that merging will not cause any data loss,
    this can be turned off by setting strict to False. 
    '''
    for k,v in new_fields.items():
        if strict:
            assert(not k in fields)
        fields[k] = v

    for k,v in new_couplings.items():
        if strict:
            assert(not k in couplings)
        couplings[k] = v


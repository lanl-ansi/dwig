import random, math

from collections import namedtuple

from common import print_err

from structure import QPUAssignment
from structure import QPUConfiguration
from structure import ChimeraCoordinate

# Generators take an instance of ChimeraQPU (qpu) and a generate a random problem and return the data as a QPUConfiguration object

def generate_ran(qpu, steps=1, feild=False):
    '''This function builds random coupleings as described by, https://arxiv.org/abs/1508.05087
    '''
    assert(isinstance(steps, int))
    assert(steps >= 1)

    choices = range(-steps, 0) + range(1, steps+1)
    choices = [float(x) for x in choices]

    fields = {}
    if feild:
        fields = {site : random.choice(choices) for site in sorted(qpu.sites)}
    couplings = {coupler : random.choice(choices) for coupler in sorted(qpu.couplers)}
    return QPUConfiguration(qpu, fields, couplings)


def generate_fl(qpu, steps=2, alpha=0.2, multicell=False, min_cycle_length=7, cycle_reject_limit=1000, cycle_sample_limit=10000):
    '''This function builds a frustrated loop problems as described by,
    https://arxiv.org/abs/1502.02098.  Because random walks are used for 
    finding cycles in the graph and constraints are applied to these cycles,
    termination of this function for all possible parameter settings is not 
    guaranteed.  Various limits are used to ensure the problem generator will 
    terminate.
    '''
    num_cycles = int(alpha*len(qpu.sites))

    incident = {}
    cycle_count = {}
    for site in qpu.sites:
        incident[site] = []
    for coupler in sorted(qpu.couplers):
        incident[coupler[0]].append(coupler)
        incident[coupler[1]].append(coupler)
        cycle_count[coupler] = 0

    site_list = sorted(list(qpu.sites))

    reject_count = 0
    cycles = []
    while len(cycles) < num_cycles:
        if reject_count >= cycle_reject_limit:
            print_err('Error: hit cycle rejection limit of {}.\ntry relaxing the cycle constraints'.format(cycle_reject_limit))
            quit()

        cycle = _build_cycle(site_list, incident, cycle_sample_limit)

        if cycle == None:
            print_err('Error: unable to find a vaild random walk cycle in {} samples.\ntry increasing the number of steps or decreasing alpha'.format(cycle_sample_limit))
            quit()

        # print_err('')
        # for coupler in cycle:
        #     print_err('{}, {}'.format(coupler[0].index, coupler[1].index))

        if len(cycle) < min_cycle_length:
            reject_count += 1
            continue

        if multicell:
            chimera_cell = cycle[0][0].chimera_cell

            second_cell = False
            for coupler in cycle:
                if coupler[0].chimera_cell != chimera_cell or coupler[1].chimera_cell != chimera_cell:
                    second_cell = True
                    break

            if not second_cell:
                reject_count += 1
                continue

        reject_count = 0

        for coupler in cycle:
            cycle_count[coupler] = cycle_count[coupler] + 1
            if cycle_count[coupler] >= steps:
                incident[coupler[0]].remove(coupler)
                incident[coupler[1]].remove(coupler)

        cycles.append(cycle)

    #for k,v in cycle_count.items():
    #    if v > 0:
    #        print_err(k, v)

    couplings = {}
    for cycle in cycles:
        for coupler in cycle:
            val = 0.0
            if coupler in couplings:
                val = couplings[coupler]
            couplings[coupler] = val - 1.0

        # make one edge in cycle different
        rand_coupler = random.choice(cycle)
        couplings[rand_coupler] = val + 1.0

    config = QPUConfiguration(qpu, {}, couplings)

    # include ground state with -1 values, so the variable domain is clearly 'spin'
    spins = { site:-1 for site in config.active_sites()}

    return QPUAssignment(config, spins, 'planted ground state, most likely non-unique')


def _build_cycle(site_list, incident, fail_limit):
    simple_cycle = None

    for tries in range(fail_limit):
        cycle = []
        touched_sites = set([])
        touched_edges = set([])
        current_site = random.choice(site_list)

        cycle_found = False
        while not cycle_found:
            touched_sites.add(current_site)

            if sum([not edge in touched_edges for edge in incident[current_site]]) <= 1:
                break

            while True:
                edge = random.choice(incident[current_site])
                if edge not in touched_edges:
                    touched_edges.add(edge)
                    break

            cycle.append(edge)

            if edge[0] == current_site:
                next_site = edge[1]
            else:
                assert(edge[1] == current_site)
                next_site = edge[0]

            if next_site in touched_sites:
                cycle_found = True
            else:
                current_site = next_site

        if cycle_found:
            # print_err('')
            # for edge in cycle:
            #     print_err(edge[0].index, edge[1].index)

            # Trim off tail edges
            simple_cycle = []
            touched_sites = set([])
            for edge in reversed(cycle):
                simple_cycle.append(edge)
                if edge[0] in touched_sites and edge[1] in touched_sites:
                    break
                else:
                    touched_sites.add(edge[0])
                    touched_sites.add(edge[1])

            # print_err('')
            # for edge in simple_cycle:
            #     print_err(edge[0].index, edge[1].index)
            break

    return simple_cycle


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


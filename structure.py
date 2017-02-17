import copy, math

from collections import namedtuple

from common import print_err


def rescale(fields, couplings, site_lb, site_ub, coupler_lb, coupler_ub):
    assert(site_lb + site_ub == 0.0)
    assert(coupler_lb + coupler_ub == 0.0)

    scaling_factor = 1.0

    for field in fields.values():
        if field != 0:
            if field < site_lb:
                scaling_factor = min(scaling_factor, site_lb/float(field))
            if field > site_ub:
                scaling_factor = min(scaling_factor, site_ub/float(field))

    for coupling in couplings.values():
        if coupling != 0:
            if coupling < coupler_lb:
                scaling_factor = min(scaling_factor, coupler_lb/float(coupling))
            if coupling > coupler_ub:
                scaling_factor = min(scaling_factor, coupler_ub/float(coupling))

    if scaling_factor < 1.0:
        print_err('info: rescaling field to [%f,%f] and couplings to [%f,%f] with scaling factor %f' % (site_lb, site_ub, coupler_lb, coupler_ub, scaling_factor))
        fields = {k:v*scaling_factor for k,v in fields.items()}
        couplings = {k:v*scaling_factor for k,v in couplings.items()}

    return fields, couplings


class QPUConfiguration(object):
    def __init__(self, qpu, fields={}, couplings={}):
        scaled_fields, scaled_couplings = rescale(fields, couplings, *(qpu.site_range+qpu.coupler_range))

        self.qpu = qpu
        self.fields = scaled_fields
        self.couplings = scaled_couplings

        for k, v in self.fields.items():
            assert(qpu.site_range[0] <= v and qpu.site_range[1] >= v)
            assert(k in qpu.sites)

        for k, v in self.couplings.items():
            assert(qpu.coupler_range[0] <= v and qpu.coupler_range[1] >= v)
            assert(k in qpu.couplers)

    def active_sites(self):
        active = set(self.fields.keys())
        active |= set([key[0] for key in self.couplings.keys()])
        active |= set([key[1] for key in self.couplings.keys()])
        return active

    def qubist_hamiltonian(self):
        lines = []
        lines.append('%d %d' % (max([site.index for site in self.qpu.sites]), len(self.fields) + len(self.couplings)))
        for i in sorted(self.fields):
            v = self.fields[i]
            lines.append('%d %d %f' % (i.index, i.index, v))
        for (i ,j) in sorted(self.couplings):
            v = self.couplings[(i,j)]
            lines.append('%d %d %f' % (i.index, j.index, v))
        return '\n'.join(lines)

    def build_dict(self):
        sorted_sites = sorted(self.active_sites(), key=lambda x: x.index)

        quadratic_terms_data = []
        for (i,j) in sorted(self.couplings.keys(), key=lambda x:(x[0].index, x[1].index)):
            v = self.couplings[(i,j)]
            assert(v != 0)
            quadratic_terms_data.append({'idx_1':i.index, 'idx_2':j.index, 'coeff':v})

        linear_terms_data = []
        for k in sorted(self.fields.keys(), key=lambda x: x.index):
            v = self.fields[k]
            assert(v != 0)
            linear_terms_data.append({'idx':k.index, 'coeff':v})

        data_dict = {
            'variable_domain': 'spin',
            'variable_idxs':[site.index for site in sorted_sites],
            'offset': 0.0,
            'linear_terms':linear_terms_data,
            'quadratic_terms':quadratic_terms_data
        }

        return data_dict


    def __str__(self):
        return 'fields: '+\
            ' '.join([str(site)+':'+str(value) for site, value in self.fields.items()]) +\
            '\ncouplings: '+' '.join(['('+str(i)+', '+str(j)+'):'+str(value) for (i,j), value in self.couplings.items()])


ChimeraCoordinate = namedtuple('ChimeraCordinate', ['row', 'col'])

class ChimeraQPU(object):
    def __init__(self, sites, couplers, chimera_degree, site_range, coupler_range, chimera_degree_view = None):
        if chimera_degree_view == None:
            self.chimera_degree_view = chimera_degree
        else:
            self.chimera_degree_view = chimera_degree_view

        self.sites = set([ChimeraSite(site, chimera_degree) for site in sites])

        site_lookup = { cn.index : cn for cn in self.sites }
        self.couplers = set([(site_lookup[i],site_lookup[j]) for i,j in couplers])
        self.chimera_degree = int(chimera_degree)
        self.site_range = site_range
        self.coupler_range = coupler_range

        self.chimera_cell_sites = {}
        for site in self.sites:
            if not site.chimera_cell in self.chimera_cell_sites:
                self.chimera_cell_sites[site.chimera_cell] = set([])
            self.chimera_cell_sites[site.chimera_cell].add(site)
        #print(self.chimera_cell_sites)

        for i,j in couplers:
            assert(i in sites)
            assert(j in sites)

        for i,j in couplers:
            assert(i != j)

    #def sites_sorted(self):
    #    return sorted(qpu.sites, key=lambda x: x.index)

    #def couplers_sorted(self):
    #    return sorted(qpu.sites, key=lambda x: x.index)

    def chimera_degree_filter(self, chimera_degree_view):
        assert(chimera_degree_view >= 1)

        filtered_sites = set([n.index for n in self.sites if n.is_chimera_degree(chimera_degree_view)])
        filtered_couplers = [(i.index, j.index) for i,j in self.couplers if (i.index in filtered_sites and j.index in filtered_sites)]

        return ChimeraQPU(filtered_sites, filtered_couplers, self.chimera_degree, self.site_range, self.coupler_range, chimera_degree_view)


    def chimera_cell(self, chimera_coordinate):
        return self.chimera_cell_coordinates(chimera_coordinate.row, chimera_coordinate.col)

    def chimera_cell_coordinates(self, chimera_row, chimera_column):
        assert(chimera_row > 0 and chimera_row <= self.chimera_degree_view)
        assert(chimera_column > 0 and chimera_column <= self.chimera_degree_view)

        return (chimera_row-1)*(self.chimera_degree) + (chimera_column-1)

    def __str__(self):
        return 'sites: '+\
            ' '.join([str(site) for site in self.sites])+'\ncouplers: '+\
            ' '.join(['('+str(i)+', '+str(j)+')' for i,j in self.couplers])


class ChimeraSite(object):
    def __init__(self, index, chimera_degree, unit_cell_size = 8):
        self.index = index
        self.chimera_cell = int(math.floor(index / unit_cell_size))
        self.chimera_row = int(math.floor(self.chimera_cell / chimera_degree))
        self.chimera_column = int(self.chimera_cell % chimera_degree)

    def is_chimera_degree(self, chimera_degree):
        return self.chimera_row+1 <= chimera_degree and self.chimera_column+1 <= chimera_degree

    def __str__(self):
        return str(self.index)

    # required so sorting works properly and problem generation is consistent
    def __lt__(self, other):
        return self.index < other.index

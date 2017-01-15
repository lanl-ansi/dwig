import copy, math

from common import print_err
from common import validate_bqp_data

def rescale(fields, couplings, site_lb, site_ub, coupler_lb, coupler_ub):
    assert(site_lb + site_ub == 0.0)
    assert(coupler_lb + coupler_ub == 0.0)

    scaling_factor = 1.0

    for field in fields.values():
        if field < site_lb:
            scaling_factor = min(scaling_factor, site_lb/field)
        if field > site_ub:
            scaling_factor = min(scaling_factor, site_ub/field)

    for coupling in couplings.values():
        if coupling < coupler_lb:
            scaling_factor = min(scaling_factor, coupler_lb/coupling)
        if coupling > coupler_ub:
            scaling_factor = min(scaling_factor, coupler_ub/coupling)

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

    def ising_dict(self):
        return self._build_dict(True, self.couplings, self.fields, 0.0)

    def bqp_dict(self):
        offset = 0
        coefficients = {}

        for site in self.active_sites():
            coefficients[(site, site)] = 0

        for k,v in self.fields.items():
            assert(v != 0)
            coefficients[(k, k)] = 2*v
            offset += -v

        for (i,j),v in self.couplings.items():
            assert(v != 0)

            assert(i.index < j.index)
            if not (i,j) in coefficients:
                coefficients[(i,j)] = 0

            coefficients[(i,j)] = coefficients[(i,j)] + 4*v
            coefficients[(i,i)] = coefficients[(i,i)] - 2*v
            coefficients[(j,j)] = coefficients[(j,j)] - 2*v
            offset += v

        linear_terms = {}
        quadratic_terms = {}

        for (i,j),v in coefficients.items():
            if v != 0.0:
                if i == j:
                    linear_terms[i] = v
                else:
                    quadratic_terms[(i,j)] = v

        return self._build_dict(False, quadratic_terms, linear_terms, offset)


    def _build_dict(self, ising, quadratic_terms, linear_terms, offset):
        sorted_sites = sorted(self.active_sites(), key=lambda x: x.index)

        quadratic_terms_data = []
        for (i,j) in sorted(quadratic_terms):
            v = quadratic_terms[(i,j)]
            assert(v != 0)
            quadratic_terms_data.append({'idx_1':i.index, 'idx_2':j.index, 'coeff':v})

        linear_terms_data = []
        for k in sorted(linear_terms):
            v = linear_terms[k]
            assert(v != 0)
            linear_terms_data.append({'idx':k.index, 'coeff':v})

        data_dict = {
            'variable_domain': 'spin' if ising else 'boolean',
            'variable_idxs':[site.index for site in sorted_sites],
            'offset': offset,
            'linear_terms':linear_terms_data,
            'quadratic_terms':quadratic_terms_data
        }

        validate_bqp_data(data_dict)
        return data_dict


    def __str__(self):
        return 'fields: '+\
            ' '.join([str(site)+':'+str(value) for site, value in self.fields.items()]) +\
            '\ncouplings: '+' '.join(['('+str(i)+', '+str(j)+'):'+str(value) for (i,j), value in self.couplings.items()])


class ChimeraQPU(object):
    def __init__(self, sites, couplers, chimera_degree, site_range, coupler_range):
        self.sites = set([ChimeraSite(site, chimera_degree) for site in sites])

        site_lookup = { cn.index : cn for cn in self.sites }
        self.couplers = set([(site_lookup[i],site_lookup[j]) for i,j in couplers])
        self.chimera_degree = chimera_degree
        self.site_range = site_range
        self.coupler_range = coupler_range

        for i,j in couplers:
            assert(i in sites)
            assert(j in sites)

        for i,j in couplers:
            assert(i != j)


    def chimera_degree_filter(self, chimera_degree):
        assert(chimera_degree >= 1)

        filtered_sites = set([n.index for n in self.sites if n.is_chimera_degree(chimera_degree)])
        filtered_couplers = [(i.index, j.index) for i,j in self.couplers if (i.index in filtered_sites and j.index in filtered_sites)]

        return ChimeraQPU(filtered_sites, filtered_couplers, chimera_degree, self.site_range, self.coupler_range)

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

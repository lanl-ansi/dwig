import copy, math

class QPUConfiguration(object):
    def __init__(qpu, field, coupling):
        pass


class ChimeraQPU(object):
    def __init__(self, nodes, edges, chimera_degree, node_range = (-2.0, 2.0), edge_range = (-1.0, 1.0)):
        self.nodes = set([ChimeraNode(node, chimera_degree) for node in nodes])
        
        node_lookup = { cn.index : cn for cn in self.nodes }
        self.edges = set([(node_lookup[i],node_lookup[j]) for i,j in edges])
        self.chimera_degree = chimera_degree
        self.node_range = node_range
        self.edge_range = edge_range

    def chimera_degree_filter(self, chimera_degree):
        assert(chimera_degree >= 1)

        filtered_nodes = set([n.index for n in self.nodes if n.is_chimera_degree(chimera_degree)])
        filtered_edges = [(i.index, j.index) for i,j in self.edges if (i.index in filtered_nodes and j.index in filtered_nodes)]

        return ChimeraQPU(filtered_nodes, filtered_edges, chimera_degree)

    def __str__(self):
        return 'nodes: '+str(self.nodes)+'\nedges: '+str(self.edges)


class ChimeraNode(object):
    def __init__(self, index, chimera_degree):
        self.index = index
        self.chimera_cell = int(math.floor(index / 8))
        self.chimera_row = int(math.floor(self.chimera_cell / chimera_degree))
        self.chimera_column = int(self.chimera_cell % chimera_degree)

    def is_chimera_degree(self, chimera_degree):
        return self.chimera_row+1 <= chimera_degree and self.chimera_column+1 <= chimera_degree

    def __str__(self):
        return 's_'+str(self.index)

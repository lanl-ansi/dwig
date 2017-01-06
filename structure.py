import copy, math


class ChimeraQPU(object):
    def __init__(self, nodes, edges, chimera_degree):
        self.nodes = set([ChimeraNode(node, chimera_degree) for node in nodes])
        self.edges = copy.deepcopy(edges)
        self.chimera_degree = chimera_degree

    def chimera_degree_filter(self, chimera_degree):
        assert(chimera_degree >= 1)

        filter_nodes = set([n.index for n in self.nodes if n.is_chimera_degree(chimera_degree)])
        filter_edges = [(i,j) for i,j in self.edges if (i in filter_nodes and j in filter_nodes)]

        return ChimeraQPU(filter_nodes, filter_edges, chimera_degree)

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


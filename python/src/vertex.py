"""Data structure to store vertex related information"""


class Vertex:
    def __init__(self,
                 weight=None,
                 degree=0,
                 bipartite_set=None,
                 opening_time=None,
                 closing_time=None,
                 depth=0,
                 parent=None,
                 ancestors=None):
        """
        Data structure to store vertex related information.
        """
        # Weight of the vertex which can used to store other problem-specific information
        self.weight = weight
        # Number of edges connected to that vertex
        self.degree = degree
        # Opening time calculated by DFS
        self.opening_time = opening_time
        # Closing time calculated by DFS
        self.closing_time = closing_time
        # Number of bipartite set to which this vertex belongs if the connected component it is in is a bipartite graph
        self.bipartite_set = bipartite_set
        # This is the depth of this vertex considering the first vertex of its connected component as the root
        self.depth = depth
        # This is the parent of the vertex in the shortest path from it to the root
        self.parent = parent
        # Logarithmic ancestors of this vertex calculated with dynamic programming for LCA with Binary Lifting
        self.ancestors = ancestors

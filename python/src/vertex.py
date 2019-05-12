
class Vertex:
    def __init__(self, weight=None, degree=0, depth=0, parent=None):
        self.weight = weight
        self.degree = degree
        # This is the depth of this vertex considering the first vertex of its connected component as the root
        self.depth = depth
        # This is the parent of the vertex in the shortest path from it to the root
        self.parent = parent
        self.opening_time = None
        self.closing_time = None

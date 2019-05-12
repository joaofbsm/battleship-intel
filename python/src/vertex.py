
class Vertex:
    def __init__(self, weight=None, degree=0, depth=0):
        self.weight = weight
        self.degree = degree
        # This is the depth of this vertex considering the first vertex of its connected component as the root
        self.depth = depth

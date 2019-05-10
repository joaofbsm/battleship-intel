
from vertex import Vertex


class Graph:
    def __init__(self, num_vertices):
        # Create adjacency list
        self.adj = [[] for _ in range(num_vertices)]

        # Set of vertices
        self.V = [Vertex() for _ in range(num_vertices)]


    def add_edge(self, u, v):
        self.adj[u].append(v)


    def update_vertex_weight(self, u, w):
        self.V[u].weight = w
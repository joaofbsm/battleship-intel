
import math
from collections import deque

from vertex import Vertex


class Graph:
    def __init__(self, num_vertices):
        # Set of vertices
        self.vertices = [Vertex() for _ in range(num_vertices)]

        # Create adjacency list
        self.adj = [[] for _ in range(num_vertices)]


    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)

        self.vertices[u].degree += 1
        self.vertices[v].degree += 1


    def update_vertex_weight(self, u, w):
        self.vertices[u].weight = w


    def connected_components_util(self, u, visited, component_vertices):
        visited[u] = True
        component_vertices.append(u)

        for v in self.adj[u]:
            if not visited[v]:
                self.connected_components_util(v, visited, component_vertices)


    def find_connected_components(self):
        visited = [False] * len(self.adj)

        connected_components = []

        for src in range(len(self.adj)):
            if not visited[src]:
                component_vertices = []
                visited[src] = True
                # Queue used for BFS
                q = deque([src])

                while q:
                    u = q.popleft()
                    component_vertices.append(u)
                    for v in self.adj[u]:
                        if not visited[v]:
                            visited[v] = True
                            q.append(v)

                connected_components.append(component_vertices)

        return connected_components


    def count_component_edges(self, vertices_ids):
        e = 0

        for v in vertices_ids:
            e += len(self.adj[v])

        # Dividing by 2 remove redundant edge counts as the graph is undirected
        return e / 2


    def get_component_max_vertex_degree(self, vertices_ids):
        max_degree = 0

        for v in vertices_ids:
            v_degree = self.vertices[v].degree
            if v_degree > max_degree:
                max_degree = v_degree

        return max_degree


    def calculate_vertices_depth(self, root):
        visited = [False] * len(self.vertices)

        visited[root] = True
        self.vertices[root].depth = 0
        q = deque([root])

        while q:
            # Pops first element (FIFO)
            u = q.popleft()
            for v in self.adj[u]:
                if not visited[v]:
                    visited[v] = True
                    self.vertices[v].depth = self.vertices[u] + 1
                    q.append(v)


    def shortest_distance_between_vertices(self, src, dest):
        # Trivial case
        if src == dest:
            return 0

        visited = [False] * len(self.vertices)
        dist = [math.inf] * len(self.vertices)

        visited[src] = True
        dist[src] = 0
        q = deque([src])

        while q:
            # Pops first element (FIFO)
            u = q.popleft()
            for v in self.adj[u]:
                if not visited[v]:
                    visited[v] = True
                    dist[v] = dist[u] + 1
                    q.append(v)

                    if v == dest:
                        return dist[v]

        # If there is no shortest path between src and dest, i.e., they are not in the same component, return None
        return None


    def get_bipartite_sets(self, src):
        bipartite_sets = [None] * len(self.vertices)
        q = deque()

        bipartite_sets[src] = 0
        q.append(src)

        while q:
            # Pops first element (FIFO)
            u = q.popleft()
            parent_set_number = bipartite_sets[u]
            for v in self.adj[u]:
                # Vertex is not in any set yet
                if bipartite_sets[v] is None:
                    bipartite_sets[v] = (parent_set_number + 1) % 2
                    q.append(v)

        return bipartite_sets


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
        time = 0

        for src in range(len(self.adj)):
            if not visited[src]:
                component_vertices = []
                # Stack used for DFS
                s = deque([src])
                self.vertices[src].bipartite_set = 0

                while s:
                    time += 1
                    u = s.pop()
                    if not visited[u]:
                        visited[u] = True
                        component_vertices.append(u)
                        # Append u again so we can calculate its closing time after all the child nodes are executed
                        s.append(u)
                        self.vertices[u].opening_time = time

                        for v in self.adj[u]:
                            if not visited[v]:
                                self.vertices[v].bipartite_set = (self.vertices[u].bipartite_set + 1) % 2
                                s.append(v)

                    else:
                        self.vertices[u].closing_time = time

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
                    self.vertices[v].depth = self.vertices[u].depth + 1
                    self.vertices[v].parent = u
                    q.append(v)


    def compute_path_to_root(self, v):
        path = [v]

        current_vertex = v

        while self.vertices[current_vertex].depth != 0:
            current_vertex = self.vertices[current_vertex].parent
            path.append(current_vertex)

        return path


    def lca(self, root, u, v):
        # Trivial case
        if u == v:
            return u

        # Cases where the vertex are the root, and, therefore, the LCA
        if root == u or root == v:
            return root

        if not self.vertices[u].path:
            self.vertices[u].path = self.compute_path_to_root(u)
        if not self.vertices[v].path:
            self.vertices[v].path = self.compute_path_to_root(v)

        path_u = self.vertices[u].path
        path_v = self.vertices[v].path

        i = -1
        # Walk on paths in the reverse order, i.e., from root to vertex
        while(path_u[i] == path_v[i]):
            ancestor = path_u[i]
            i -= 1
            # Reached end of a path
            if ancestor == u or ancestor == v:
                break

        # This is the least common ancestor
        return ancestor

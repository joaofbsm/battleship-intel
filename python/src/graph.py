
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

        path_u = self.compute_path_to_root(u)
        path_v = self.compute_path_to_root(v)

        i = -1
        # Walk on paths in the reverse order, i.e., from root to vertex
        while(path_u[i] == path_v[i]):
            ancestor = path_u[i]
            i -= 1
            # Reached end of a path
            if ancestor == u or ancestor == v:
                break

        # This is the lowest common ancestor
        return ancestor


    def dfs_for_lca(self, src):
        # As there are no cycles in a tree, there is no need to check if a vertex was already visited
        s = deque([src])
        self.vertices[src].depth = 0
        self.vertices[src].parent = src

        log_num_vertices = int(math.ceil(math.log(len(self.vertices), 2)))

        while s:
            u = s.pop()
            self.vertices[u].ancestors = [-1] * (log_num_vertices + 1)
            self.vertices[u].ancestors[0] = self.vertices[u].parent

            for i in range(1, log_num_vertices + 1):
                calculated_vertex = self.vertices[u].ancestors[i - 1]
                self.vertices[u].ancestors[i] = self.vertices[calculated_vertex].ancestors[i - 1]

            for v in self.adj[u]:
                if v != self.vertices[u].parent:
                    s.append(v)
                    self.vertices[v].depth = self.vertices[u].depth + 1
                    self.vertices[v].parent = u


    def lca_with_binary_lifting(self, root, u, v):
        # Trivial cases
        if u == v:
            return u
        elif u == root or v == root:
            return root

        log_num_vertices = int(math.ceil(math.log(len(self.vertices), 2)))

        # Swap vertices to execute the ancestor search on the one who is deepest on the tree
        if self.vertices[u].depth < self.vertices[v].depth:
            aux = u
            u = v
            v = aux

        for i in range(log_num_vertices, -1, -1):
            if (self.vertices[u].depth - (2 ** i)) >= self.vertices[v].depth:
                u = self.vertices[u].ancestors[i]

            if u == v:
                return u

        for i in range(log_num_vertices, -1, -1):
            if self.vertices[u].ancestors[i] != self.vertices[v].ancestors[i]:
                u = self.vertices[u].ancestors[i]
                v = self.vertices[v].ancestors[i]

        return self.vertices[u].ancestors[0]
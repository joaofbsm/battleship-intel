"""General graph data structure"""

import math
from collections import deque

from vertex import Vertex


class Graph:
    def __init__(self, num_vertices):
        """
        General graph data structure.
        """
        # Set of vertices
        self.vertices = [Vertex() for _ in range(num_vertices)]

        # Create adjacency list
        self.adj = [[] for _ in range(num_vertices)]


    def add_edge(self, u, v):
        """
        Due to specification restrictions, the edge (u, v) will not appear during the creation of the graph, so we can
        create both ends of the edge right now.
        """
        self.adj[u].append(v)
        self.adj[v].append(u)

        self.vertices[u].degree += 1
        self.vertices[v].degree += 1


    def update_vertex_weight(self, u, w):
        """
        Update the weight of a vertex, which can used to store other problem-specific information.
        """
        self.vertices[u].weight = w


    def find_connected_components(self):
        """
        Using an iterative DFS, walks through the graph, computing and storing important information about vertices that
        can be used latter.
        """
        visited = [False] * len(self.adj)
        # Each item is a list of vertex ids that represent a connect component
        connected_components = []
        time = 0

        for src in range(len(self.adj)):
            if not visited[src]:
                component_vertices = []
                # Stack used for DFS
                s = deque([src])
                # There are only two bipartite sets, represented by integers 0 and 1
                self.vertices[src].bipartite_set = 0

                while s:
                    time += 1
                    u = s.pop()
                    if not visited[u]:
                        # Contrary to BFS, visiting occurs when executing, not when discovering
                        visited[u] = True
                        component_vertices.append(u)
                        # Push u again so we can calculate its closing time after all the child nodes are executed
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
        """
        Count the number of edges in a component which vertices ids are contained in vertices_ids
        """
        e = 0

        for v in vertices_ids:
            e += len(self.adj[v])

        # Dividing by 2 remove redundant edge counts as the graph is undirected
        return e / 2


    def get_component_max_vertex_degree(self, vertices_ids):
        """
        Iterate over all vertices in the component and returns the max vertex degree found.
        """
        max_degree = 0

        for v in vertices_ids:
            v_degree = self.vertices[v].degree
            if v_degree > max_degree:
                max_degree = v_degree

        return max_degree


    def compute_depths_and_ancestors(self, root):
        """
        Computes the depths of each vertex in a connected component in relation to the root vertex received, and also a
        list of the log |V| + 1 "binary" ancestors of the vertices.. This is a modified iterative DFS procedure that
        don't need to mark vertices as visited, thus saving some time.
        """
        # As there are no cycles in a tree, there is no need to check if a vertex was already visited
        s = deque([root])
        self.vertices[root].depth = 0
        self.vertices[root].parent = root

        log_num_vertices = int(math.ceil(math.log(len(self.vertices), 2)))

        while s:
            u = s.pop()
            # Initialize ancestors list
            self.vertices[u].ancestors = [-1] * (log_num_vertices + 1)
            self.vertices[u].ancestors[0] = self.vertices[u].parent

            # Uses dynamic programming to calculate the ancestors list
            for i in range(1, log_num_vertices + 1):
                calculated_vertex = self.vertices[u].ancestors[i - 1]
                self.vertices[u].ancestors[i] = self.vertices[calculated_vertex].ancestors[i - 1]

            for v in self.adj[u]:
                # This condition prevents the traversal of an already traversed edge
                if v != self.vertices[u].parent:
                    s.append(v)
                    # Creation of a path based on the parent vertex
                    self.vertices[v].depth = self.vertices[u].depth + 1
                    self.vertices[v].parent = u


    def lca_with_binary_lifting(self, root, u, v):
        """
        Finds the Lowest Common Ancestor (LCA) with the assistance of the Binary Lifting idea. This procedure is faster
        than a simple LCA.
        """
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

        # Finds the ancestor of u which is at the same depth as v
        for i in range(log_num_vertices, -1, -1):
            if (self.vertices[u].depth - (2 ** i)) >= self.vertices[v].depth:
                u = self.vertices[u].ancestors[i]

        # If v is an ancestor of u, then v is the LCA of the pair
        if u == v:
            return v

        # Finds the vertex closest to the root which is not a common ancestor between u and v, but which parent is
        for i in range(log_num_vertices, -1, -1):
            if self.vertices[u].ancestors[i] != self.vertices[v].ancestors[i]:
                u = self.vertices[u].ancestors[i]
                v = self.vertices[v].ancestors[i]

        return self.vertices[u].ancestors[0]


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

        for v in range(len(self.adj)):
            if not visited[v]:
                component_vertices = []

                self.connected_components_util(v, visited, component_vertices)

                connected_components.append(component_vertices)

        return connected_components


    def cycle_util(self, u, parent, visited):
        # Mark the current node as visited
        visited[u] = True

        # Recur for all the vertices adjacent to this vertex
        for i in range(len(self.adj[u])):
            if not visited[self.adj[u][i]]:
                if self.cycle_util(self.adj[u][i], u, visited):
                    return True
            elif self.adj[u][i] != parent:
                return True

        return False


    def is_component_cyclic(self, src):
        visited = [False] * len(self.adj)

        if self.cycle_util(src, None, visited):
            return True

        return False


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
            max_degree = v_degree if v_degree > max_degree else max_degree

        return max_degree

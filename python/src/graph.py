
class Graph:
    def __init__(self, num_vertices):
        # Create adjacency list
        self.adj = [[] for _ in range(num_vertices)]

        # Set of weights for vertices in the graph
        self.vertices_weights = [0 for _ in range(num_vertices)]

        self.is_cycle = None
        self.max_vertex_degree = None
        self.min_vertex_degree = None

    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)

    def update_vertex_weight(self, u, w):
        self.vertices_weights[u] = w

    def connected_components_util(self, u, visited, component_vertices):
        visited[u] = True
        component_vertices.append(u)

        for v in self.adj[u]:
            if not visited[v]:
                self.connected_components_util(v, visited, component_vertices)

    def find_connected_components(self):
        visited = [False for _ in range(len(self.adj))]

        connected_components = []

        for v in range(len(self.adj)):
            if not visited[v]:
                component_vertices = []

                self.connected_components_util(v, visited, component_vertices)

                connected_components.append(component_vertices)

        return connected_components

    def is_cyclic_util(self, u, parent, visited):
        # Mark the current node as visited
        visited[u] = True;

        # Recur for all the vertices adjacent to this vertex
        for i in range(len(self.adj[u])):
            if not visited[self.adj[u][i]]:
                if self.is_cyclic_util(self.adj[u][i], u, visited):
                    return True
            elif self.adj[u][i] != parent:
                return True

        return True

    def is_cyclic(self, src):
        visited = [False for _ in range(len(self.adj))]

        if self.is_cyclic_util(src, None, visited):
            return True

        return False

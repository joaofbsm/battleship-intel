"""Abstraction that encapsulates methods to generate intel about ships in the enemy fleet"""

from graph import Graph


class Ship():
    def __init__(self, vertices_ids):
        """
        Abstraction that encapsulates methods to generate intel about ships in the enemy fleet.
        """
        self.vertices_ids = vertices_ids
        # The type will be represented by an integer in the interval [0, 3]
        self.ship_type = None


    def identify_ship(self, g: Graph):
        """
        Identify ship type, attributing the findings to self.ship_type,
        """
        # As the ship subgraph is undirected and unweighted, if it contains more than |V| - 1 edges, a cycle exists
        # This method is effective because we can detect a cycle in O(|E|) using a operation we already needed
        num_edges = g.count_component_edges(self.vertices_ids)

        # Component contains no cycles
        if len(self.vertices_ids) - 1 == num_edges:
            # As the minimum number of posts is 5, if a component's vertices have degree at most 2 it's a Reconhecimento
            if g.get_component_max_vertex_degree(self.vertices_ids) == 2:
                self.ship_type = 0  # Reconhecimento
            else:
                self.ship_type = 1  # Frigata
        # Component contains cycles
        else:
            # Transportador's number of edges is always equals the number of vertices
            if len(self.vertices_ids) != num_edges:
                self.ship_type = 2  # Bombardeiro
            else:
                self.ship_type = 3  # Transportador


    def compute_advantage_time_lower_bound(self, g: Graph, min_fleet_advantage):
        """
        Compute the lower bound of the advantage time, considering that the minimum advantage time already obtained
        is min_fleet_advantage. If during any calculation the value surpasses min_fleet_advantage, the calculation is
        immediately stopped, as we are only look for the lower bound.
        """

        # To prevent overhead in the comparison, compute the "real" advantage time only once
        # This process is derived from Yamanaka et. al. - Swapping Labeled Tokens on Graphs
        adjusted_min_fleet_advantage = min_fleet_advantage * 2

        # One specific heuristic per type of ship to reduce calculation time
        heuristic_per_ship = {
           0: self.compute_tree_advantage,
           1: self.compute_tree_advantage,
           2: self.compute_bombardeiro_advantage,
           3: self.compute_transportador_advantage
        }

        advantage_time = heuristic_per_ship[self.ship_type](g, adjusted_min_fleet_advantage)

        return advantage_time


    def compute_tree_advantage(self, g: Graph, adjusted_min_fleet_advantage):
        """
        Heuristic to accelerate the computation of ships that have a tree like structure, which are the Reconhecimento
        and Frigata. It relies on the fact that for trees, the Lowest Common Ancestor (LCA) with Binary Lifting
        algorithm can be computed in O(lg n), where n is the number of vertices in it. We need to compute the depths and
        ancestors first using a DFS though, but the time is still linear in the number of vertices for a sparse graph.
        """
        advantage_time = 0

        root = self.vertices_ids[0]
        # Compute the depth and the binary lifting ancestor list for each vertex in the component
        g.compute_depths_and_ancestors(root)

        for v in self.vertices_ids:
            dest = g.vertices[v].weight
            lca = g.lca_with_binary_lifting(root, v, dest)

            # Compute by distance between vertices by summing their distances to a common ancestor and removing this
            # ancestors distance from the root twice to "connect" the two paths.
            advantage_time += g.vertices[v].depth + g.vertices[dest].depth - 2 * g.vertices[lca].depth

            # Check to prevent overcalculating the advantage time
            if advantage_time >= adjusted_min_fleet_advantage:
                return int(adjusted_min_fleet_advantage / 2)

        return int(advantage_time / 2)


    def compute_bombardeiro_advantage(self, g: Graph, adjusted_min_fleet_advantage):
        """
        Heuristic to accelerate the computation of a Bombardeiro ship advantage time. It relies on the fact that, even
        though every type of ship is a bipartite graph, the only complete bipartite is the Bombardeiro, and for each
        vertex, depending on the bipartite set they are located, the distance to any other one will be at most 2.
        """
        advantage_time = 0

        for v in self.vertices_ids:
            dest = g.vertices[v].weight
            # If the current vertex is already the destination, the advantage time doesn't change
            if v != dest:
                # As the ship is a complete bipartite, the distance between vertices in the same set is 2
                if g.vertices[v].bipartite_set == g.vertices[dest].bipartite_set:
                    advantage_time += 2
                # For vertices in different sets, the distance is 1
                else:
                    advantage_time += 1

            # Check to prevent overcalculating the advantage time
            if advantage_time >= adjusted_min_fleet_advantage:
                return int(adjusted_min_fleet_advantage / 2)

        return int(advantage_time / 2)


    def compute_transportador_advantage(self, g: Graph, adjusted_min_fleet_advantage):
        """
        Heuristic to accelerate the computation of a Transportador ship advantage time. From each vertex we can go both
        left or right to find the destination node, as the graph is cyclic. We then calculate both distances by first
        subtracting the opening times for the vertex found in DFS, and afterwards calculating the distance by going
        traversing the other path, which can be smaller.
        """
        advantage_time = 0

        for v in self.vertices_ids:
            dest = g.vertices[v].weight

            # Similar to Reconhecimento's heuristic but now we have two possible paths
            dist1 = abs(g.vertices[v].opening_time - g.vertices[dest].opening_time)
            dist2 = len(self.vertices_ids) - dist1

            advantage_time += min(dist1, dist2)

            # Check to prevent overcalculating the advantage time
            if advantage_time >= adjusted_min_fleet_advantage:
                return int(adjusted_min_fleet_advantage / 2)

        return int(advantage_time / 2)

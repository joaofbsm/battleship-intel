
from graph import Graph


class Ship():
    def __init__(self, vertices_ids):
        self.vertices_ids = vertices_ids
        self.ship_type = None


    def identify_ship(self, g: Graph):
        num_edges = g.count_component_edges(self.vertices_ids)
        # If so, the graph contains no cycles
        if len(self.vertices_ids) - 1 == num_edges:
            if g.get_component_max_vertex_degree(self.vertices_ids) == 2:
                self.ship_type = 0  # Reconhecimento
            else:
                self.ship_type = 1  # Frigata
        else:
            if len(self.vertices_ids) != num_edges:
                self.ship_type = 2  # Bombardeiro
            else:
                self.ship_type = 3  # Transportador


    def compute_advantage_time_lower_bound(self, g: Graph, min_fleet_advantage):
        # To prevent overhead in the comparison, compute the "real" advantage time only once
        adjusted_min_fleet_advantage = min_fleet_advantage * 2

        heuristic_per_ship = {
           0: self.compute_reconhecimento_advantage,
           1: self.compute_frigata_advantage,
           2: self.compute_bombardeiro_advantage,
           3: self.compute_transportador_advantage
        }

        advantage_time = heuristic_per_ship[self.ship_type](g, adjusted_min_fleet_advantage)

        return advantage_time


    def compute_general_advantage(self, g: Graph, adjusted_min_fleet_advantage):
        """Computation of ship advantage time not specific to any type of ship"""
        advantage_time = 0

        for v in self.vertices_ids:
            dist = g.shortest_distance_between_vertices(v, g.vertices[v].weight)
            advantage_time += dist

            if advantage_time >= adjusted_min_fleet_advantage:
                return int(adjusted_min_fleet_advantage / 2)

        return int(advantage_time / 2)


    def compute_reconhecimento_advantage(self, g: Graph, adjusted_min_fleet_advantage):
        advantage_time = 0

        for v in self.vertices_ids:
            dest = g.vertices[v].weight
            advantage_time += abs(g.vertices[v].opening_time - g.vertices[dest].opening_time)

            if advantage_time >= adjusted_min_fleet_advantage:
                return int(adjusted_min_fleet_advantage / 2)

        return int(advantage_time / 2)


    def compute_frigata_advantage(self, g: Graph, adjusted_min_fleet_advantage):
        advantage_time = 0

        root = self.vertices_ids[0]
        g.dfs_for_lca(root)

        for v in self.vertices_ids:
            dest = g.vertices[v].weight
            lca = g.lca_with_binary_lifting(root, v, dest)

            advantage_time += g.vertices[v].depth + g.vertices[dest].depth - 2 * g.vertices[lca].depth

            if advantage_time >= adjusted_min_fleet_advantage:
                return int(adjusted_min_fleet_advantage / 2)

        return int(advantage_time / 2)


    def compute_bombardeiro_advantage(self, g: Graph, adjusted_min_fleet_advantage):
        advantage_time = 0

        for v in self.vertices_ids:
            dest = g.vertices[v].weight
            # If the current vertex is already the destination, the advantage time doesn't change
            if v != dest:
                # As the ship is a complete bipartite, the distance between vertices in the same set is 2
                if g.vertices[v].bipartite_set == g.vertices[dest].bipartite_set:
                    advantage_time += 2
                # For vertex in different sets, the distance is 1
                else:
                    advantage_time += 1

            if advantage_time >= adjusted_min_fleet_advantage:
                return int(adjusted_min_fleet_advantage / 2)

        return int(advantage_time / 2)


    def compute_transportador_advantage(self, g: Graph, adjusted_min_fleet_advantage):
        advantage_time = 0

        for v in self.vertices_ids:
            dest = g.vertices[v].weight

            # Similar to Reconhecimento's heuristic but now we have two possible paths
            dist1 = abs(g.vertices[v].opening_time - g.vertices[dest].opening_time)
            dist2 = len(self.vertices_ids) - dist1

            advantage_time += min(dist1, dist2)

            if advantage_time >= adjusted_min_fleet_advantage:
                return int(adjusted_min_fleet_advantage / 2)

        return int(advantage_time / 2)

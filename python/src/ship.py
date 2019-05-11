
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
        advantage_time = 0

        # To remove overhead in the comparison, compute the "real" advantage time only once
        adjusted_min_fleet_advantage = min_fleet_advantage * 2

        # If the ship is a Bombardeiro, i.e., a complete bipartite graph, we can calculate the advantage time faster
        if self.ship_type == 2:
            bipartite_sets = g.get_bipartite_sets(self.vertices_ids[0])
            for v in self.vertices_ids:
                dest = g.vertices[v].weight
                # If the current vertex is already the destination, the advantage time doesn't change
                if v != dest:
                    # As the ship is a complete bipartite, the distance between vertices in the same set is 2
                    if bipartite_sets[v] == bipartite_sets[dest]:
                        advantage_time += 2
                    # For vertex in different sets, the distance is 1
                    else:
                        advantage_time += 1

                if advantage_time >= adjusted_min_fleet_advantage:
                    return min_fleet_advantage

        else:
            for v in self.vertices_ids:
                dist = g.shortest_distance_between_vertices(v, g.vertices[v].weight)
                advantage_time += dist

                if advantage_time >= adjusted_min_fleet_advantage:
                    return min_fleet_advantage

        return int(advantage_time / 2)




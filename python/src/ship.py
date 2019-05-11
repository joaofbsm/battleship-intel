
from graph import Graph


class Ship():
    def __init__(self, vertices_ids):
        self.vertices_ids = vertices_ids
        self.ship_type = None


    def identify_ship(self, g: Graph):
        num_edges = g.count_component_edges(self.vertices_ids)
        # If so, the graph contains no cycles
        if len(self.vertices_ids) - 1  == num_edges:
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

        for v in self.vertices_ids:
            dist = g.shortest_distance_between_vertices(v, g.vertices[v].weight)
            advantage_time += dist

            if advantage_time >= adjusted_min_fleet_advantage:
                return min_fleet_advantage

        return int(advantage_time / 2)





from graph import Graph


class Ship():
    def __init__(self, vertices_ids):
        self.vertices_ids = vertices_ids
        self.ship_type = None
        self.advantage_time = 0


    def identify_ship(self, g: Graph):
        has_cycles = g.is_component_cyclic(self.vertices_ids[0])
        if not has_cycles:
            if g.get_component_max_vertex_degree(self.vertices_ids) == 2:
                self.ship_type = 0  # Reconhecimento
            else:
                self.ship_type = 1  # Frigata
        else:
            if len(self.vertices_ids) != g.count_component_edges(self.vertices_ids):
                self.ship_type = 2  # Bombardeiro
            else:
                self.ship_type = 3  # Transportador

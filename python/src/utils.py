"""Miscellaneous utility methods"""

import sys

from graph import Graph


def create_graph_from_file(input_file):

    with open(input_file) as f:
        # Read radar information header
        num_combat_posts, num_possible_teleports = [int(i) for i in f.readline().split()]

        g = Graph(num_combat_posts)

        try:
            for _ in range(num_possible_teleports):
                line = f.readline()
                # Adjust all vertex indices for 0-indexing
                a, b = [int(i) - 1 for i in line.split()]
                g.add_edge(a, b)
        except Exception as e:
            print('Exception occurred while parsing possible teleports\n{}'.format(e), file=sys.stderr)

        try:
            for _ in range(num_combat_posts):
                line = f.readline()
                # Adjust all vertex indices for 0-indexing
                c, d = [int(i) - 1 for i in line.split()]
                g.update_vertex_weight(c, d)
        except Exception as e:
            print('Exception occurred while parsing combat posts\n{}'.format(e), file=sys.stderr)

    return g


def sort_ships_by_size(ships, reverse=False):
    return sorted(ships, key=lambda s: len(s.vertices_ids), reverse=reverse)


def group_and_sort_ships(ships, reverse=False):
    reco = sort_ships_by_size([s for s in ships if s.ship_type == 0], reverse=reverse)
    frig = sort_ships_by_size([s for s in ships if s.ship_type == 1], reverse=reverse)
    bomb = sort_ships_by_size([s for s in ships if s.ship_type == 2], reverse=reverse)
    tran = sort_ships_by_size([s for s in ships if s.ship_type == 3], reverse=reverse)

    return reco, frig, bomb, tran


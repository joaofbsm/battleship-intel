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





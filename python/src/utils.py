"""Miscellaneous utility methods"""

import sys

import graph

def create_graph_from_file(input_file):

    with open(input_file) as f:
        num_combat_posts, num_possible_teleports = f.readline().split()

        G = Graph(num_combat_posts);

        for m in range(num_possible_teleports):
            line = f.readline()
            try:
                a, b = line.split()
                G.add_edge(a, b)
            except AttributeError as e:
                if str(e) == "'NoneType' object has no attribute 'split'":
                    print('There are missing teleports on the input file', file=sys.stderr)

        for n in range(num_combat_posts):
            line = f.readline()
            try:
                c, d = line.split()
                G.add_vertex_weight(c, d)
            except AttributeError as e:
                if str(e) == "'NoneType' object has no attribute 'split'":
                    print('There are missing combat posts on the input file', file=sys.stderr)

    return G




"""Analyse enemy fleet and create intel report"""

import argparse
import math
import os

import utils
from ship import Ship


def main(args):
    # Create output directory if it does not exists already
    output_dir = os.path.abspath(os.path.join(args.output_file_path, os.pardir))
    os.makedirs(output_dir, exist_ok=True)

    # Create the fleet graph using radar information contained in the input file
    fleet = utils.create_graph_from_file(args.input_file_path)

    # Detect the ships (connected components) in the fleet (graph)
    ships = [Ship(component) for component in fleet.find_connected_components()]

    # Identify ships and count their quantity by type
    ship_types = [0] * 4
    for s in ships:
        s.identify_ship(fleet)
        ship_types[s.ship_type] += 1
    print(*ship_types, sep=' ')

    min_fleet_advantage = math.inf

    # Sort ships in crescent order of quantity of vertices for faster computing
    ships = utils.sort_ships_by_size(ships)

    #for s in [i for i in ships if i.ship_type in [0, 1, 2, 3]]:
    for s in ships:
        min_fleet_advantage = s.compute_advantage_time_lower_bound(fleet, min_fleet_advantage)

    print(min_fleet_advantage)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyse enemy fleet and create intel report.')

    parser.add_argument('-i', '--input-file-path', type=str, dest='input_file_path',
                        help='Path to input file where the radar data can be found')
    parser.add_argument('-o', '--output-file-path', type=str, dest='output_file_path',
                        help='Path to output file to which the generated intel report must be saved.')

    main(parser.parse_args())

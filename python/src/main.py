"""Analyse enemy fleet and create intel report"""

import argparse
import os

import utils
from ship import Ship


def main(args):
    # Create output directory if it does not exists already
    output_dir = os.path.abspath(os.path.join(args.output_file_path, os.pardir))
    os.makedirs(output_dir, exist_ok=True)

    fleet = utils.create_graph_from_file(args.input_file_path)

    ships = [Ship(component) for component in fleet.find_connected_components()]

    ship_types = [0] * 4
    for s in ships:
        s.identify_ship(fleet)
        ship_types[s.ship_type] += 1

    print(*ship_types, sep=' ')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyse enemy fleet and create intel report.')

    parser.add_argument('-i', '--input-file-path', type=str, dest='input_file_path',
                        help='Path to input file where the radar data can be found')
    parser.add_argument('-o', '--output-file-path', type=str, dest='output_file_path',
                        help='Path to output file to which the generated intel report must be saved.')

    main(parser.parse_args())

"""Analyse radar data and create intel report about enemy fleet"""

import math

import utils
from ship import Ship


def main():
    # Create the fleet graph using radar information contained in the input file
    fleet = utils.create_graph_from_stdin()

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

    # Compute lower bound for advantage time
    for s in ships:
        min_fleet_advantage = s.compute_advantage_time_lower_bound(fleet, min_fleet_advantage)
    print(min_fleet_advantage)


if __name__ == '__main__':
    main()

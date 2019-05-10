#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include "graph.h"

using namespace std;

// TODO: Move this to utils.cpp
Graph create_graph_from_file(char *path_to_file) {
    ifstream f;
    f.open(path_to_file);

    // These are equivalent to the number of vertices and edges in the graph, respectively
    int num_combat_posts, num_possible_teleports;

    string line;

    getline(f, line);
    istringstream iss(line);
    iss >> num_combat_posts >> num_possible_teleports;

    int m=0;
    Graph g = Graph(num_combat_posts);
    
    while (m < num_possible_teleports and getline(f, line)) {
        int a, b;
        istringstream iss(line);
        if (!(iss >> a >> b)) { 
            cout << "Error parsing input file.";
        }
        
        g.add_edge(a, b);

        m++;
    }

    // Loops num_combat_posts times
    while (getline(f, line)) {
        int c, d;
        istringstream iss(line);
        if (!(iss >> c >> d)) {
            cout << "Error parsing input file.";
        }

        g.add_vertex_state(c, d);
    }

    f.close();

    return g;
}


int main(int argc, char *argv[]) {
    Graph g = create_graph_from_file(argv[1]);

    // g.print_adj_list();

    cout << "===========\n";

    // g.print_vertices_state();

    cout << "===========\n";

    g.find_connected_components();
    // g.print_connected_components();

    cout << "===========\n";

    g.identify_enemy_fleet();
    g.print_enemy_fleet_numbers();

    return 0;
}
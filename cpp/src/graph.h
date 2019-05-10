#ifndef GRAPH_H
#define GRAPH_H

#include <iostream> 
#include <vector> 
#include <list> 

using namespace std; 
  
// Graph class represents a undirected graph 
// using adjacency list representation 
class Graph { 
    int V;    // No. of vertices 
    int E;    // No. of edges
  
    // Pointer to an array containing adjacency lists 
    vector<int> *adj; 
  
    // One dimensional array indexed by vertex number which contains its state
    int *vertices_state;

    // Groups of vertices that are connected subgraphs
    vector< vector<int> > connected_components;

    // Type of each ship in the fleet respective to connected_components
    vector<int> fleet_ships

    // Advantage time for each ship in the fleet respective to fleet_ships
    vector<int> advantage_time

    // Quantity of each type of ship in the enemy fleet
    int enemy_fleet_numbers[4] = {0};

    // Depth First Search recursive function
    void connected_components_util(int u, vector<bool> &visited, vector<int> &connected_vertices);
public: 
    Graph(int V);   // Constructor 
    void add_vertex_state(int actual_post, int correct_post);
    void add_edge(int v, int w); 
    void find_connected_components(); 
    void print_adj_list();
    void print_vertices_state();
    void print_connected_components();
    bool is_cyclic_util(int u, int parent, vector<bool> &visited);
    bool is_cyclic(int src);
    bool is_bipartite(int src);
    int count_num_edges(vector<int> graph);
    vector<int> get_vertex_degrees(vector<int> graph);
    int identify_battleship_type(vector<int> subgraph);
    void identify_enemy_fleet();
    void print_enemy_fleet_numbers();
    void calculate_fleet_advantage_time();
}; 

#endif
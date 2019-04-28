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

    // Depth First Search recursive function
    void DFS_visit(int u, vector<bool> &visited, vector<int> &connected_vertices);
public: 
    Graph(int V);   // Constructor 
    void add_vertex_state(int actual_post, int correct_post);
    void add_edge(int v, int w); 
    void find_connected_components(); 
    void print_adj_list();
    void print_vertices_state();
    void print_connected_components();
    bool is_bipartite(int src);
}; 

#endif
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

    // Depth First Search functions
    void DFS_visit(int u, vector<bool> &visited); 
    void DFS();
public: 
    Graph(int V);   // Constructor 
    void add_vertex_state(int actual_post, int correct_post);
    void add_edge(int v, int w); 
    void connected_components(); 
    void print_adj_list();
    void print_vertices_state();
    bool is_bipartite(int src);
}; 

#endif
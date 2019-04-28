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
    list<int> *adj; 
  
    // Bidimensional vector containing pairs of states
    vector< vector<int> > vertices_state;

    // DFS recursive function
    void DFS_visit(int v, bool visited[]); 
public: 
    Graph(int V);   // Constructor 
    void add_vertex_state(int actual_post, int correct_post);
    void add_edge(int v, int w); 
    void connected_components(); 
}; 

#endif
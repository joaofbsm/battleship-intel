#ifndef GRAPH_H
#define GRAPH_H

#include <iostream> 
#include <vector> 
#include <list> 

using namespace std; 
  
// Graph class represents a undirected graph 
// using adjacency list representation 
class Graph 
{ 
    int V;    // No. of vertices 
    int E;    // No. of edges
  
    // Pointer to an array containing adjacency lists 
    list<int> *adj; 
  
    // A function used by DFS 
    void DFSUtil(int v, bool visited[]); 
public: 
    Graph(int V);   // Constructor 
    void addEdge(int v, int w); 
    void connectedComponents(); 
}; 

#endif
#include <iostream> 
#include <vector> 
#include <list>
#include "graph.h"

using namespace std; 

Graph::Graph(int V) { 
    this->V = V; 
    adj = new vector<int>[V + 1]();
    vertices_state = new int[V + 1]();
} 


// Method to print connected components in an undirected graph 
void Graph::connected_components() { 
    // Mark all the vertices as not visited 
    vector<bool> visited(V, false);
    for(int v = 0; v < V; v++) 
        visited[v] = false; 
  
    for (int v=0; v<V; v++) 
    { 
        if (visited[v] == false) 
        { 
            // print all reachable vertices from v 
            DFS_visit(v, visited); 
  
            cout << "\n"; 
        } 
    }
} 


void Graph::DFS_visit(int u, vector<bool> &visited) { 
    // Mark the current node as visited and print it 
    visited[u] = true; 
    cout << u << " "; 
  
    // Recur for all the vertices adjacent to this vertex 
    for (int i=0; i<adj[u].size(); i++) 
            if (visited[adj[u][i]] == false) 
                DFS_visit(adj[u][i], visited); 
} 


// This function does DFS_visit() for all unvisited vertices
void Graph::DFS() 
{ 
    vector<bool> visited(V, false); 
    for (int u=0; u<V; u++) 
        if (visited[u] == false) 
            DFS_visit(u, visited); 
} 


// Method to add an undirected edge 
void Graph::add_edge(int v, int w) { 
    adj[v].push_back(w); 
    adj[w].push_back(v); 
}


void Graph::add_vertex_state(int actual_post, int correct_post) {
    vertices_state[actual_post] = correct_post;
}


void Graph::print_adj_list() {
    for (int i; i < V; i++) {
        for (int j:adj[i]) {
            cout << j << ' ';
        }
        cout << "\n";    
    }    
}

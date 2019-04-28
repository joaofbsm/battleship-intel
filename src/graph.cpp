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
    bool *visited = new bool[V]; 
    for(int v = 0; v < V; v++) 
        visited[v] = false; 
  
    for (int v=0; v<V; v++) 
    { 
        if (visited[v] == false) 
        { 
            // print all reachable vertices 
            // from v 
            DFS_visit(v, visited); 
  
            cout << "\n"; 
        } 
    } 
} 


void Graph::DFS_visit(int v, bool visited[]) { 
    // Mark the current node as visited and print it 
    visited[v] = true; 
    cout << v << " "; 
  
    // Recur for all the vertices 
    // adjacent to this vertex 
    vector<int>::iterator i; 
    for(i = adj[v].begin(); i != adj[v].end(); ++i) 
        if(!visited[*i]) 
            DFS_visit(*i, visited); 
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

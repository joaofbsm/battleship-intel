#include <iostream> 
#include <vector> 
#include <list>
#include <queue> 
#include "graph.h"

using namespace std; 

Graph::Graph(int V) { 
    this->V = V; 
    adj = new vector<int>[V + 1]();
    vertices_state = new int[V + 1]();
} 


// DFS to find connected components in an undirected graph 
void Graph::find_connected_components() { 
    // Mark all the vertices as not visited 
    vector<bool> visited (V + 1, false);

    for (int v = 1; v < V + 1; v++) { 
        if (visited[v] == false) { 
            vector<int> connected_vertices;

            // print all reachable vertices from v 
            DFS_visit(v, visited, connected_vertices);

            connected_components.push_back(connected_vertices);
        }
    }
} 


void Graph::DFS_visit(int u, vector<bool> &visited, vector<int> &connected_vertices) { 
    // Mark the current node as visited and print it 
    visited[u] = true;
    connected_vertices.push_back(u);
  
    // Recur for all the vertices adjacent to this vertex 
    for (int i = 0; i < adj[u].size(); i++) {
        if (visited[adj[u][i]] == false) {
            DFS_visit(adj[u][i], visited, connected_vertices); 
        }
    }
} 


// Method to add an undirected edge 
void Graph::add_edge(int v, int w) { 
    adj[v].push_back(w); 
    adj[w].push_back(v); 
}


void Graph::add_vertex_state(int actual_post, int correct_post) {
    vertices_state[actual_post] = correct_post;
}


// Prints the adjacency list
void Graph::print_adj_list() {
    for (int i = 1; i < V + 1; i++) {
        cout << i << ": ";
        for (int j: adj[i]) {
            cout << j << " ";
        }
        cout << "\n";    
    }
}


// Prints the array of vertices states
void Graph::print_vertices_state() {
    for (int i = 1; i < V + 1; i++) {
        cout << i << ": " << vertices_state[i] << "\n";
    }
}


void Graph::print_connected_components() {
    for (auto const& c: connected_components) {
        for(auto const& v: c) {
            cout << v << " ";
        }
        cout << "\n";
    }
}


// Tries to paint the graph with only two colors to check if it is bipartite
bool Graph::is_bipartite(int src) {
    // Start all vertices with no color (-1)
    vector<int> vertices_color (V + 1, -1);

    queue<int> q;
    // Push source vertex to the queue
    q.push(src);

    // Paint source vertex with the first color
    vertices_color[src] = 0;

    // Traverse connected component
    while (!q.empty()) { 
        // Dequeue a vertex from queue
        int u = q.front(); 
        q.pop(); 

        for(auto const& v: adj[u]) {
            // Discovered vertice that is not yet colored
            if (vertices_color[v] == -1) {
                // Paints adjacent vertex with different color
                vertices_color[v] = (vertices_color[u] + 1) % 2;
                q.push(v);
            }
            // Two adjacent vertices have the same color
            else if (vertices_color[v] == vertices_color[u]) {
                return false;
            }
        }
    }

    return true;
}

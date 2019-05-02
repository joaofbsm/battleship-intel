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


// Method to add an undirected edge 
void Graph::add_edge(int v, int w) { 
    adj[v].push_back(w); 
    adj[w].push_back(v); 
}


void Graph::add_vertex_state(int actual_post, int correct_post) {
    vertices_state[actual_post] = correct_post;
}


// DFS to find connected components in an undirected graph 
void Graph::find_connected_components() { 
    // Mark all the vertices as not visited 
    vector<bool> visited (V + 1, false);

    for (int v = 1; v < V + 1; v++) { 
        if (visited[v] == false) { 
            vector<int> connected_vertices;

            // print all reachable vertices from v 
            connected_components_util(v, visited, connected_vertices);

            connected_components.push_back(connected_vertices);
        }
    }
} 


void Graph::connected_components_util(int u, vector<bool> &visited, vector<int> &connected_vertices) { 
    // Mark the current node as visited and add it to the component
    visited[u] = true;
    connected_vertices.push_back(u);
  
    // Recur for all the vertices adjacent to this vertex 
    for (int i = 0; i < adj[u].size(); i++) {
        if (visited[adj[u][i]] == false) {
            connected_components_util(adj[u][i], visited, connected_vertices); 
        }
    }
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


bool Graph::is_cyclic_util(int u, int parent, vector<bool> &visited) {
    // Mark the current node as visited
    visited[u] = true;

    // cout << "Current vertex: " << u << " Parent: " << parent << "\n"; 
  
    // Recur for all the vertices adjacent to this vertex 
    for (int i = 0; i < adj[u].size(); i++) {
        if (visited[adj[u][i]] == false) {
            if (is_cyclic_util(adj[u][i], u, visited)) {
                return true;
            }
        }
        else if (adj[u][i] != parent) {
            // cout << "Is cycle! Current: " << adj[u][i] << " Parent: " << parent << "\n";
            return true;
        }
    }

    return false;
}


bool Graph::is_cyclic(int src) {
    // Mark all the vertices as not visited 
    vector<bool> visited (V + 1, false);
    
    if(is_cyclic_util(src, -1, visited)) {
        return true;
    }

    return false;
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


int Graph::count_num_edges(vector<int> graph) {
    int E = 0;
    for (auto const& v: graph) {
        for (auto const& u: adj[v]) {
            if (u > v) {
                E++;
            }
        }
    }

    return E;
}


vector<int> Graph::get_vertex_degrees(vector<int> graph) {
    vector<int> degrees;

    for (int v : graph) {
        degrees.push_back(adj[v].size());
    }

    return degrees;
}

int Graph::identify_battleship_type(vector<int> subgraph) {
    // Map of ship type and return of this function:
    // Reconhecimento : 0
    // Frigata : 1
    // Bombardeiro : 2
    // Transportador : 3

    // If there is a cycle can be a Bombardeiro or a Transportador battleship
    if (is_cyclic(subgraph.front())) {
        // Is Transportador
        if (subgraph.size() == count_num_edges(subgraph)) {
            cout << "Transportador: " << subgraph.front() << "\n";
            return 3;
        }
        // Is Bombardeiro
        else {
            cout << "Bombardeiro: " << subgraph.front() << "\n";
            return 2;
        }
    }
    // If there is no cycle it can be a Frigata or a Reconhecimento battleship
    else {
        vector<int> degrees = get_vertex_degrees(subgraph);

        // Is Reconhecimento
        if (count_if(degrees.begin(), degrees.end(), [](int x) { return (x == 2); }) == subgraph.size() - 2
            and count_if(degrees.begin(), degrees.end(), [](int x) { return (x == 1); }) == 2) {
            cout << "Reconhecimento: " << subgraph.front() << "\n";
            return 0;
        }
        // Is Frigata
        else {
            cout << "Frigata: " << subgraph.front() << "\n";
            return 1;
        }
    }
}


void Graph::identify_enemy_fleet() {
    for (auto subgraph : connected_components) {
        enemy_fleet_numbers[identify_battleship_type(subgraph)]++;
    }
}


void Graph::print_enemy_fleet_numbers() {
    for (auto i : enemy_fleet_numbers) {
        cout << i << " ";
    }
    cout << "\n";
}

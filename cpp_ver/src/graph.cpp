#include "graph.hpp"
#include "json.hpp"
#include <fstream>
#include <stdexcept>

using json = nlohmann::json;

// Constructor: Initializes graph with given number of vertices
Graph::Graph(int vertices) : V(vertices), adj(vertices) {}

// Adds an undirected edge between two vertices with given weight
void Graph::addEdge(int u, int v, int weight) {
    adj[u].emplace_back(v, weight);
    adj[v].emplace_back(u, weight);
    E++;
}

// Loads graph from a JSON file
Graph Graph::loadFromJSON(const std::string& filepath) {
    std::ifstream file(filepath);
    if (!file.is_open()) {
        throw std::runtime_error("Could not open file: " + filepath);
    }

    json data;
    file >> data;

    // Create graph with number of nodes from JSON
    int num_nodes = data["nodes"].size();
    Graph graph(num_nodes);

    // Add all edges from JSON to graph
    for (const auto& edge : data["edges"]) {
        int u = edge[0];
        int v = edge[1];
        int weight = edge[2];
        graph.addEdge(u, v, weight);
    }

    return graph;
}

// Returns the adjacency list representation of the graph
const std::vector<std::vector<std::pair<int, int>>>& Graph::getAdjList() const { 
    return adj; 
}

// Returns the number of vertices in the graph
int Graph::getV() const { 
    return V; 
}

// Returns the number of edges in the graph
int Graph::getE() const { 
    return E; 
}
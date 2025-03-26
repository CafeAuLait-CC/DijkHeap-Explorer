#pragma once
#include <vector>
#include <string>
#include <utility>

class Graph {
    int V;
    int E = 0;
    std::vector<std::vector<std::pair<int, int>>> adj;

public:
    Graph(int vertices);
    void addEdge(int u, int v, int weight);
    static Graph loadFromJSON(const std::string& filepath);
    
    const std::vector<std::vector<std::pair<int, int>>>& getAdjList() const;
    int getV() const;
    int getE() const;
};
#include "dijkstra.hpp"
#include "binary_heap.hpp"
#include "d_heap.hpp"
#include <chrono>

using namespace std::chrono;

// Dijkstra's algorithm implementation using std::priority_queue (binary heap)
std::vector<int> dijkstraPriorityQueue(const Graph& graph, int src) {
    int V = graph.getV();
    const auto& adj = graph.getAdjList();
    
    // Initialize distances to infinity
    std::vector<int> dist(V, INT_MAX);
    dist[src] = 0;
    
    // Min-heap using std::priority_queue
    std::priority_queue<std::pair<int, int>, std::vector<std::pair<int, int>>, std::greater<std::pair<int, int>>> pq;
    pq.push({0, src});
    
    while (!pq.empty()) {
        auto current = pq.top();
        pq.pop();
        int u = current.second;
        int current_dist = current.first;
        
        // Skip if we've already found a better path
        if (current_dist > dist[u]) continue;
        
        // Relax all adjacent edges
        for (const auto& edge : adj[u]) {
            int v = edge.first;
            int weight = edge.second;
            
            if (dist[v] > dist[u] + weight) {
                dist[v] = dist[u] + weight;
                pq.push({dist[v], v});
            }
        }
    }
    
    return dist;
}

// Dijkstra's algorithm implementation using D-Heap
std::vector<int> dijkstraDHeap(const Graph& graph, int src, int d) {
    int V = graph.getV();
    const auto& adj = graph.getAdjList();
    
    std::vector<int> dist(V, INT_MAX);
    dist[src] = 0;
    
    DHeap heap(V, d);
    heap.push(0, src);
    
    while (!heap.empty()) {
        auto current = heap.pop();
        int u = current.second;
        int current_dist = current.first;
        
        if (current_dist > dist[u]) continue;
        
        for (const auto& edge : adj[u]) {
            int v = edge.first;
            int weight = edge.second;
            
            if (dist[v] > dist[u] + weight) {
                dist[v] = dist[u] + weight;
                if (heap.contains(v)) {
                    heap.decrease_key(v, dist[v]);
                } else {
                    heap.push(dist[v], v);
                }
            }
        }
    }
    return dist;
}

// Dijkstra's algorithm implementation using Fibonacci Heap
std::vector<int> dijkstraFibonacciHeap(const Graph& graph, int src) {
    int V = graph.getV();
    const auto& adj = graph.getAdjList();
    std::vector<int> dist(V, INT_MAX);
    dist[src] = 0;
    
    FibonacciHeap fh(V);
    // Initialize heap with all vertices
    for (int i = 0; i < V; ++i) {
        fh.push(i == src ? 0 : INT_MAX, i);
    }
    
    while (!fh.empty()) {
        auto current = fh.pop();
        int u = current.second;
        
        // Relax all adjacent edges
        for (const auto& edge : adj[u]) {
            int v = edge.first;
            int weight = edge.second;
            
            if (dist[v] > dist[u] + weight) {
                dist[v] = dist[u] + weight;
                fh.decrease_key(v, dist[v]);
            }
        }
    }
    return dist;
}

// Dijkstra's algorithm implementation using Radix Heap
std::vector<int> dijkstraRadixHeap(const Graph& graph, int src) {
    int V = graph.getV();
    const auto& adj = graph.getAdjList();
    
    std::vector<int> dist(V, INT_MAX);
    dist[src] = 0;
    
    OptimizedRadixHeap rh;
    rh.push({0, src});
    
    while (!rh.empty()) {
        auto current = rh.pop();
        int u = current.second;
        int current_dist = current.first;
        
        if (current_dist > dist[u]) continue;
        
        for (const auto& edge : adj[u]) {
            int v = edge.first;
            int weight = edge.second;
            
            if (dist[v] > dist[u] + weight) {
                dist[v] = dist[u] + weight;
                rh.push({dist[v], v});
            }
        }
    }
    
    return dist;
}

// Measures the execution time of a Dijkstra algorithm implementation
double time_algorithm(std::function<std::vector<int>(const Graph&, int)> algo, 
                     const Graph& g, int src, int iterations) {
    // Warm-up runs
    for (int i = 0; i < 3; ++i) algo(g, src);
    
    // Measure performance over multiple iterations
    double total = 0;
    for (int i = 0; i < iterations; ++i) {
        auto start = high_resolution_clock::now();
        auto result = algo(g, src);
        auto end = high_resolution_clock::now();
        total += duration_cast<microseconds>(end-start).count();
    }
    return total / (iterations * 1000.0);  // Return time in milliseconds
}
#include "graph.hpp"
#include "dijkstra.hpp"
#include <iostream>
#include <algorithm>
#include <string>

int main(int argc, char* argv[]) {
    try {
        // Check for correct number of arguments
        if (argc != 2) {
            std::cerr << "Usage: " << argv[0] << " <graph_file.json>\n";
            return 1;
        }

        std::string filepath = argv[1];
        // Load graph from JSON file
        Graph g = Graph::loadFromJSON(filepath);
        int src = 0;  // Source vertex for Dijkstra's algorithm

        // Calculate recommended d for D-Heap based on average degree
        int m = g.getE();
        int n = g.getV();
        int d_recommended = (2 * m) / n;

        std::cout << "Graph loaded with " << n << " vertices, " << m << " edges\n";
        std::cout << "Using D-Heap with d = " << d_recommended << "\n";
        
        // Run Dijkstra's algorithm with different heap implementations and measure performance
        std::cout << "\nRunning Dijkstra with Binary Heap...\n";
        double time_bh = time_algorithm(dijkstraPriorityQueue, g, src);
        auto dist_bh = dijkstraPriorityQueue(g, src);
        
        std::cout << "Running Dijkstra with D-Heap...\n";
        double time_dh = time_algorithm([&](const Graph& g, int src) { 
            return dijkstraDHeap(g, src, d_recommended); 
        }, g, src);
        auto dist_dh = dijkstraDHeap(g, src, d_recommended);

        std::cout << "Running Dijkstra with Fibonacci Heap...\n";
        double time_fh = time_algorithm(dijkstraFibonacciHeap, g, src);
        auto dist_fh = dijkstraFibonacciHeap(g, src);

        std::cout << "Running Dijkstra with Radix Heap...\n";
        double time_rh = time_algorithm(dijkstraRadixHeap, g, src);
        auto dist_rh = dijkstraRadixHeap(g, src);
        
        // Verify that all implementations produce the same results
        bool results_match = equal(dist_bh.begin(), dist_bh.end(), dist_rh.begin()) && 
                           equal(dist_bh.begin(), dist_bh.end(), dist_fh.begin()) &&
                           std::equal(dist_bh.begin(), dist_bh.end(), dist_dh.begin());

        // Print performance results
        std::cout << "\nPerformance Results:\n";
        std::cout << "-------------------\n";
        std::cout << "Binary Heap:  " << time_bh << " ms\n";
        std::cout << "D-Heap (d=" << d_recommended << "): " << time_dh << " ms\n";
        std::cout << "Radix Heap:   " << time_rh << " ms\n";
        std::cout << "Fibonacci Heap: " << time_fh << " ms\n";
        
        // Print speed comparisons
        std::cout << "\nSpeed Ratios:\n";
        std::cout << "Binary/Radix: " << time_bh/time_rh << "x\n";
        std::cout << "Binary/Fib:   " << time_bh/time_fh << "x\n";
        std::cout << "Binary/DHeap:    " << time_bh/time_dh << "x\n";
        // std::cout << "\nResults match: " << (results_match ? "YES" : "NO") << std::endl;

        // Print sample distances for verification
        std::cout << "\nSample distances (first 10 vertices):\n";
        for (int i = 0; i < fmin(10, g.getV()); ++i) {
            std::cout << "Vertex " << i << ": BH=" << dist_bh[i] 
                 << ", RH=" << dist_rh[i] 
                 << ", FH=" << dist_fh[i] << "\n";
        }
                
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    return 0;
}
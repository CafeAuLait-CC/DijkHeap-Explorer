#pragma once
#include "graph.hpp"
#include "fibonacci_heap.hpp"
#include "radix_heap.hpp"
#include "d_heap.hpp"
#include <vector>
#include <functional>
#include <queue>

std::vector<int> dijkstraPriorityQueue(const Graph& graph, int src);
std::vector<int> dijkstraFibonacciHeap(const Graph& graph, int src);
std::vector<int> dijkstraRadixHeap(const Graph& graph, int src);
std::vector<int> dijkstraDHeap(const Graph& graph, int src, int d);

double time_algorithm(std::function<std::vector<int>(const Graph&, int)> algo, 
                     const Graph& g, int src, int iterations = 5);
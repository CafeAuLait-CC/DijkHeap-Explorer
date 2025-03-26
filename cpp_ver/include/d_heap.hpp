#pragma once
#include <vector>
#include <utility>
#include <algorithm>
#include <stdexcept>

class DHeap {
    int d;
    std::vector<std::pair<int, int>> heap;
    std::vector<int> vertex_to_index;

    int parent(int i) const;
    int first_child(int i) const;
    void heapify_up(int index);
    void heapify_down(int index);

public:
    DHeap(int max_vertices, int heap_degree);
    bool contains(int vertex) const {
        return vertex_to_index[vertex] != -1;
    }
    void push(int distance, int vertex);
    std::pair<int, int> pop();
    void decrease_key(int vertex, int new_distance);
    bool empty() const;
};
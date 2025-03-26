#pragma once
#include <vector>
#include <utility>
#include <stdexcept>

class BinaryHeap {
    std::vector<std::pair<int, int>> heap;
    std::vector<int> vertex_to_index;

    void heapify_up(int index);
    void heapify_down(int index);

public:
    BinaryHeap(int max_vertices);
    void push(int distance, int vertex);
    std::pair<int, int> pop();
    void decrease_key(int vertex, int new_distance);
    bool empty() const;
};
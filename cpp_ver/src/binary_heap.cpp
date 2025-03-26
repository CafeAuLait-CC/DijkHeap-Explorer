#include "binary_heap.hpp"

// Constructor: Initializes the heap with given maximum vertices
BinaryHeap::BinaryHeap(int max_vertices) : vertex_to_index(max_vertices, -1) {}

// Inserts a new element into the heap
void BinaryHeap::push(int distance, int vertex) {
    if (vertex_to_index[vertex] != -1) return;
    heap.emplace_back(distance, vertex);
    vertex_to_index[vertex] = heap.size() - 1;
    heapify_up(heap.size() - 1);
}

// Removes and returns the minimum element from the heap
std::pair<int, int> BinaryHeap::pop() {
    if (heap.empty()) throw std::runtime_error("Heap is empty");
    
    auto min = heap[0];
    vertex_to_index[min.second] = -1;

    if (heap.size() > 1) {
        heap[0] = heap.back();
        vertex_to_index[heap[0].second] = 0;
    }
    heap.pop_back();

    if (!heap.empty()) heapify_down(0);
    return min;
}

// Decreases the key of a vertex in the heap
void BinaryHeap::decrease_key(int vertex, int new_distance) {
    int index = vertex_to_index[vertex];
    if (index == -1 || new_distance > heap[index].first) return;
    heap[index].first = new_distance;
    heapify_up(index);
}

// Checks if the heap is empty
bool BinaryHeap::empty() const { 
    return heap.empty(); 
}

// Restores heap property by moving a node up the tree
void BinaryHeap::heapify_up(int index) {
    while (index > 0) {
        int parent = (index - 1) / 2;
        if (heap[index].first < heap[parent].first) {
            std::swap(heap[index], heap[parent]);
            vertex_to_index[heap[index].second] = index;
            vertex_to_index[heap[parent].second] = parent;
            index = parent;
        } else {
            break;
        }
    }
}

// Restores heap property by moving a node down the tree
void BinaryHeap::heapify_down(int index) {
    int left, right, smallest;
    while (true) {
        left = 2 * index + 1;
        right = 2 * index + 2;
        smallest = index;

        // Find the smallest child
        if (left < heap.size() && heap[left].first < heap[smallest].first) {
            smallest = left;
        }
        if (right < heap.size() && heap[right].first < heap[smallest].first) {
            smallest = right;
        }

        // Swap with smallest child if necessary
        if (smallest != index) {
            std::swap(heap[index], heap[smallest]);
            vertex_to_index[heap[index].second] = index;
            vertex_to_index[heap[smallest].second] = smallest;
            index = smallest;
        } else {
            break;
        }
    }
}
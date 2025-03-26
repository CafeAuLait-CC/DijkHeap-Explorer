#include "d_heap.hpp"

// Constructor: Initializes the heap with given maximum vertices and degree
DHeap::DHeap(int max_vertices, int heap_degree) 
    : d(std::max(2, heap_degree)), vertex_to_index(max_vertices, -1) {}

// Inserts a new element into the heap
void DHeap::push(int distance, int vertex) {
    if (vertex_to_index[vertex] != -1) return;
    heap.emplace_back(distance, vertex);
    vertex_to_index[vertex] = heap.size() - 1;
    heapify_up(heap.size() - 1);
}

// Removes and returns the minimum element from the heap
std::pair<int, int> DHeap::pop() {
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
void DHeap::decrease_key(int vertex, int new_distance) {
    int index = vertex_to_index[vertex];
    if (index == -1 || new_distance > heap[index].first) return;
    heap[index].first = new_distance;
    heapify_up(index);
}

// Checks if the heap is empty
bool DHeap::empty() const { 
    return heap.empty(); 
}

// Returns the parent index of a given node
int DHeap::parent(int i) const { 
    return (i - 1) / d; 
}

// Returns the first child index of a given node
int DHeap::first_child(int i) const { 
    return d * i + 1; 
}

// Restores heap property by moving a node up the tree
void DHeap::heapify_up(int index) {
    while (index > 0) {
        int p = parent(index);
        if (heap[index].first < heap[p].first) {
            std::swap(heap[index], heap[p]);
            vertex_to_index[heap[index].second] = index;
            vertex_to_index[heap[p].second] = p;
            index = p;
        } else {
            break;
        }
    }
}

// Restores heap property by moving a node down the tree
void DHeap::heapify_down(int index) {
    int smallest = index;
    int child = first_child(index);
    int last_child = std::min(child + d, (int)heap.size());

    // Find the smallest child
    for (int i = child; i < last_child; ++i) {
        if (heap[i].first < heap[smallest].first) {
            smallest = i;
        }
    }

    // Swap with smallest child if necessary
    if (smallest != index) {
        std::swap(heap[index], heap[smallest]);
        vertex_to_index[heap[index].second] = index;
        vertex_to_index[heap[smallest].second] = smallest;
        heapify_down(smallest);
    }
}
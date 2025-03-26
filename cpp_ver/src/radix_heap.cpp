#include "radix_heap.hpp"

// Constructor: Initializes the buckets and sets initial size to 0
OptimizedRadixHeap::OptimizedRadixHeap() : buckets(BUCKETS) {}

// Checks if the heap is empty
bool OptimizedRadixHeap::empty() const { 
    return size_ == 0; 
}

// Returns the number of elements in the heap
size_t OptimizedRadixHeap::size() const { 
    return size_; 
}

// Inserts a new element into the heap
void OptimizedRadixHeap::push(std::pair<int, int> item) {
    int bucket = fastFindBucket(item.first);
    buckets[bucket].push(item);
    size_++;
}

// Removes and returns the minimum element from the heap
std::pair<int, int> OptimizedRadixHeap::pop() {
    if (empty()) throw std::runtime_error("Heap empty");
    
    // Find the first non-empty bucket
    int bucket = 0;
    while (buckets[bucket].empty()) bucket++;
    
    // If bucket is not 0, redistribute its elements and recursively call pop
    if (bucket > 0) {
        last_deleted = findMinInBucket(bucket);
        redistribute(bucket);
        return pop();
    }
    
    // Return the element from bucket 0
    auto item = buckets[0].front();
    buckets[0].pop();
    size_--;
    last_deleted = item.first;
    return item;
}

// Fast method to determine the bucket for a given key
int OptimizedRadixHeap::fastFindBucket(int key) const {
    if (key <= last_deleted) return 0;
    unsigned diff = key - last_deleted;
    #ifdef __GNUC__
    // Use built-in function for counting leading zeros if available
    return __builtin_clz(diff) ? 0 : (31 - __builtin_clz(diff)) + 1;
    #else
    // Fallback method for finding the most significant bit
    int msb = 0;
    while (diff >>= 1) msb++;
    return msb + 1;
    #endif
}

// Finds the minimum value in a given bucket
int OptimizedRadixHeap::findMinInBucket(int bucket) {
    int min_val = INT_MAX;
    std::queue<std::pair<int, int>> temp;
    
    // Iterate through all elements in the bucket to find the minimum
    while (!buckets[bucket].empty()) {
        auto item = buckets[bucket].front();
        min_val = std::min(min_val, item.first);
        temp.push(item);
        buckets[bucket].pop();
    }
    
    // Restore the bucket's contents
    buckets[bucket].swap(temp);
    return min_val;
}

// Redistributes elements from a bucket to appropriate buckets
void OptimizedRadixHeap::redistribute(int bucket) {
    while (!buckets[bucket].empty()) {
        auto item = buckets[bucket].front();
        buckets[bucket].pop();
        int new_bucket = fastFindBucket(item.first);
        buckets[new_bucket].push(item);
    }
}
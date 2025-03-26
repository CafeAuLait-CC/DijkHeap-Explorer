#pragma once
#include <vector>
#include <queue>
#include <utility>
#include <climits>
#include <stdexcept>

class OptimizedRadixHeap {
    static constexpr int BUCKETS = sizeof(int) * 8 + 1;
    int last_deleted = 0;
    std::vector<std::queue<std::pair<int, int>>> buckets;
    size_t size_ = 0;

    int fastFindBucket(int key) const;
    int findMinInBucket(int bucket);
    void redistribute(int bucket);

public:
    OptimizedRadixHeap();
    bool empty() const;
    size_t size() const;
    void push(std::pair<int, int> item);
    std::pair<int, int> pop();
};
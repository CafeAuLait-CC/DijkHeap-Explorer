#pragma once
#include <vector>
#include <utility>
#include <algorithm>
#include <cmath>
#include <stdexcept>

class FibonacciHeap {
    struct Node {
        int key;
        int vertex;
        int degree = 0;
        bool marked = false;
        Node* parent = nullptr;
        Node* child = nullptr;
        Node* left = nullptr;
        Node* right = nullptr;

        Node(int k, int v) : key(k), vertex(v) {
            left = right = this;
        }
    };

    Node* min_node = nullptr;
    int size = 0;
    std::vector<Node*> node_table;

    void link(Node* y, Node* x);
    void consolidate();
    void cut(Node* x, Node* y);
    void cascading_cut(Node* y);
    void delete_tree(Node* node);

public:
    FibonacciHeap(int max_vertices);
    ~FibonacciHeap();
    void clear();
    bool empty() const;
    int get_size() const;
    void push(int key, int vertex);
    std::pair<int, int> pop();
    void decrease_key(int vertex, int new_key);
};
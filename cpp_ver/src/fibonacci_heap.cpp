#include "fibonacci_heap.hpp"

// Constructor: Initializes the heap with a given maximum number of vertices
FibonacciHeap::FibonacciHeap(int max_vertices) : node_table(max_vertices, nullptr) {}

// Destructor: Cleans up all heap nodes
FibonacciHeap::~FibonacciHeap() {
    clear();
}

// Clears all nodes from the heap
void FibonacciHeap::clear() {
    if (!min_node) return;
    
    // Delete all nodes in the root list
    Node* current = min_node;
    do {
        Node* next = current->right;
        delete_tree(current->child);
        delete current;
        current = next;
    } while (current != min_node);
    
    min_node = nullptr;
    size = 0;
    std::fill(node_table.begin(), node_table.end(), nullptr);
}

// Checks if the heap is empty
bool FibonacciHeap::empty() const { 
    return min_node == nullptr; 
}

// Returns the number of elements in the heap
int FibonacciHeap::get_size() const { 
    return size; 
}

// Inserts a new element into the heap
void FibonacciHeap::push(int key, int vertex) {
    if (node_table[vertex] != nullptr) {
        throw std::runtime_error("Vertex already exists in heap");
    }
    
    // Create new node and add it to the root list
    Node* node = new Node(key, vertex);
    node_table[vertex] = node;
    
    if (!min_node) {
        min_node = node;
    } else {
        node->left = min_node;
        node->right = min_node->right;
        min_node->right->left = node;
        min_node->right = node;
        
        // Update min node if necessary
        if (node->key < min_node->key) {
            min_node = node;
        }
    }
    size++;
}

// Removes and returns the minimum element from the heap
std::pair<int, int> FibonacciHeap::pop() {
    if (!min_node) throw std::runtime_error("Heap is empty");

    Node* z = min_node;
    std::pair<int, int> result(z->key, z->vertex);
    node_table[z->vertex] = nullptr;

    // Add children of min node to root list
    if (z->child) {
        Node* child = z->child;
        do {
            Node* next_child = child->right;
            child->parent = nullptr;
            child->left = min_node;
            child->right = min_node->right;
            min_node->right->left = child;
            min_node->right = child;
            child = next_child;
        } while (child != z->child);
    }

    // Remove min node from root list
    z->left->right = z->right;
    z->right->left = z->left;

    if (z == z->right) {
        min_node = nullptr;
    } else {
        min_node = z->right;
        consolidate();
    }

    delete z;
    size--;
    return result;
}

// Decreases the key of a node in the heap
void FibonacciHeap::decrease_key(int vertex, int new_key) {
    Node* node = node_table[vertex];
    if (!node || new_key > node->key) {
        return;
    }

    node->key = new_key;
    Node* parent = node->parent;

    // Perform cut and cascading cut if necessary
    if (parent && node->key < parent->key) {
        cut(node, parent);
        cascading_cut(parent);
    }

    // Update min node if necessary
    if (!min_node || node->key < min_node->key) {
        min_node = node;
    }
}

// Links one tree to another as a child
void FibonacciHeap::link(Node* y, Node* x) {
    // Remove y from root list
    y->left->right = y->right;
    y->right->left = y->left;

    // Make y a child of x
    y->parent = x;
    if (!x->child) {
        x->child = y;
        y->left = y->right = y;
    } else {
        y->left = x->child;
        y->right = x->child->right;
        x->child->right->left = y;
        x->child->right = y;
    }
    x->degree++;
    y->marked = false;
}

// Consolidates trees in the heap to maintain Fibonacci heap properties
void FibonacciHeap::consolidate() {
    if (!min_node) return;

    std::vector<Node*> A(ceil(log2(size)) + 1, nullptr);
    std::vector<Node*> roots;
    Node* current = min_node;
    
    // Collect all root nodes
    do {
        roots.push_back(current);
        current = current->right;
    } while (current != min_node);

    // Combine trees of same degree
    for (Node* w : roots) {
        Node* x = w;
        int d = x->degree;
        while (A[d]) {
            Node* y = A[d];
            if (x->key > y->key) {
                std::swap(x, y);
            }
            link(y, x);
            A[d] = nullptr;
            d++;
        }
        A[d] = x;
    }

    // Rebuild root list
    min_node = nullptr;
    for (Node* a : A) {
        if (a) {
            if (!min_node) {
                min_node = a;
                min_node->left = min_node->right = min_node;
            } else {
                a->left = min_node;
                a->right = min_node->right;
                min_node->right->left = a;
                min_node->right = a;
                if (a->key < min_node->key) {
                    min_node = a;
                }
            }
        }
    }
}

// Cuts a node from its parent and adds it to root list
void FibonacciHeap::cut(Node* x, Node* y) {
    if (x->right == x) {
        y->child = nullptr;
    } else {
        x->left->right = x->right;
        x->right->left = x->left;
        if (y->child == x) {
            y->child = x->right;
        }
    }
    y->degree--;

    // Add x to root list
    x->left = min_node;
    x->right = min_node->right;
    min_node->right->left = x;
    min_node->right = x;

    x->parent = nullptr;
    x->marked = false;
}

// Performs cascading cut operation up the tree
void FibonacciHeap::cascading_cut(Node* y) {
    Node* z = y->parent;
    if (z) {
        if (!y->marked) {
            y->marked = true;
        } else {
            cut(y, z);
            cascading_cut(z);
        }
    }
}

// Recursively deletes a tree of nodes
void FibonacciHeap::delete_tree(Node* node) {
    if (!node) return;
    Node* current = node;
    do {
        Node* next = current->right;
        delete_tree(current->child);
        delete current;
        current = next;
    } while (current != node);
}
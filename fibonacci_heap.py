class FibonacciHeapNode:
    """
    A node in the Fibonacci Heap.
    """
    def __init__(self, priority, value):
        self.priority = priority  # Priority of the node
        self.value = value        # Value stored in the node
        self.degree = 0           # Number of children
        self.marked = False       # Marked flag for cascading cuts
        self.parent = None        # Parent node
        self.child = None         # Child node
        self.left = self          # Left sibling (circular doubly linked list)
        self.right = self         # Right sibling (circular doubly linked list)

class FibonacciHeap:
    """
    A Fibonacci Heap implementation.
    """
    def __init__(self):
        self.min_node = None  # Pointer to the minimum node
        self.count = 0        # Number of nodes in the heap

    def is_empty(self):
        """Check if the heap is empty."""
        return self.min_node is None

    def push(self, priority, value):
        """
        Insert a value with a given priority into the heap.
        
        :param priority: The priority of the value.
        :param value: The value to insert.
        """
        new_node = FibonacciHeapNode(priority, value)
        
        # Add the new node to the root list
        if self.min_node is not None:
            new_node.left = self.min_node
            new_node.right = self.min_node.right
            self.min_node.right.left = new_node
            self.min_node.right = new_node
            
            # Update the minimum node if necessary
            if new_node.priority < self.min_node.priority:
                self.min_node = new_node
        else:
            self.min_node = new_node
        
        self.count += 1

    def pop(self):
        """
        Remove and return the value with the smallest priority.
        
        :return: The value with the smallest priority.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty FibonacciHeap.")
        
        min_node = self.min_node
        value = min_node.value
        
        # Move all children of the minimum node to the root list
        if min_node.child is not None:
            child = min_node.child
            while True:
                next_child = child.right
                child.left.right = child.right
                child.right.left = child.left
                child.left = self.min_node
                child.right = self.min_node.right
                self.min_node.right.left = child
                self.min_node.right = child
                child.parent = None
                if next_child == min_node.child:
                    break
                child = next_child
        
        # Remove the minimum node from the root list
        min_node.left.right = min_node.right
        min_node.right.left = min_node.left
        
        if min_node == min_node.right:
            self.min_node = None
        else:
            self.min_node = min_node.right
            self._consolidate()
        
        self.count -= 1
        return value, min_node.priority

    def _consolidate(self):
        """
        Consolidate the heap to ensure no two roots have the same degree.
        """
        degree_table = [None] * self.count
        nodes_to_visit = []
        
        # Collect all root nodes
        current = self.min_node
        while True:
            nodes_to_visit.append(current)
            current = current.right
            if current == self.min_node:
                break
        
        for node in nodes_to_visit:
            degree = node.degree
            while degree_table[degree] is not None:
                other = degree_table[degree]
                if node.priority > other.priority:
                    node, other = other, node
                self._link(other, node)
                degree_table[degree] = None
                degree += 1
            degree_table[degree] = node
        
        # Find the new minimum node
        self.min_node = None
        for node in degree_table:
            if node is not None:
                if self.min_node is None or node.priority < self.min_node.priority:
                    self.min_node = node

    def _link(self, child, parent):
        """
        Link two trees by making one the child of the other.
        
        :param child: The node to become the child.
        :param parent: The node to become the parent.
        """
        # Remove child from the root list
        child.left.right = child.right
        child.right.left = child.left
        
        # Make child a child of parent
        if parent.child is not None:
            child.left = parent.child
            child.right = parent.child.right
            parent.child.right.left = child
            parent.child.right = child
        else:
            parent.child = child
            child.left = child
            child.right = child
        
        child.parent = parent
        parent.degree += 1
        child.marked = False

    def __len__(self):
        """Return the number of elements in the heap."""
        return self.count

    def __str__(self):
        """Return a string representation of the heap."""
        if self.is_empty():
            return "Empty FibonacciHeap"
        
        result = []
        current = self.min_node
        while True:
            result.append(f"(Priority: {current.priority}, Value: {current.value})")
            current = current.right
            if current == self.min_node:
                break
        return " -> ".join(result)
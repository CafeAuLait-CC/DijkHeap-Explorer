class FibonacciHeapNode:
    """
    A node in the Fibonacci Heap.
    
    Attributes:
        priority: Priority value of the node.
        value: Value stored in the node.
        degree: Number of children.
        marked: Flag for cascading cuts.
        parent: Parent node reference.
        child: Child node reference.
        left: Left sibling in circular doubly linked list.
        right: Right sibling in circular doubly linked list.
    """
    def __init__(self, priority, value):
        self.priority = priority
        self.value = value
        self.degree = 0
        self.marked = False
        self.parent = None
        self.child = None
        self.left = self  # Circular reference to self initially
        self.right = self

class FibonacciHeap:
    """
    A Fibonacci Heap implementation with amortized O(1) insert and decrease_key.
    
    Attributes:
        min_node: Pointer to the minimum node in the root list.
        count: Number of nodes in the heap.
    """
    def __init__(self):
        self.min_node = None
        self.count = 0

    def is_empty(self):
        """Check if the heap is empty."""
        return self.min_node is None

    def push(self, priority, value):
        """
        Insert a value with given priority into the heap.
        
        Args:
            priority: The priority of the value.
            value: The value to insert.
        """
        new_node = FibonacciHeapNode(priority, value)
        
        # Add to root list
        if self.min_node is not None:
            new_node.left = self.min_node
            new_node.right = self.min_node.right
            self.min_node.right.left = new_node
            self.min_node.right = new_node
            
            # Update min if necessary
            if new_node.priority < self.min_node.priority:
                self.min_node = new_node
        else:
            self.min_node = new_node
        
        self.count += 1

    def pop(self):
        """
        Remove and return the value with the smallest priority.
        
        Returns:
            Tuple of (value, priority) of the minimum element.
            
        Raises:
            IndexError: If the heap is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty FibonacciHeap.")
        
        min_node = self.min_node
        value = min_node.value
        
        # Move all children to root list
        if min_node.child is not None:
            child = min_node.child
            while True:
                next_child = child.right
                # Remove from child list
                child.left.right = child.right
                child.right.left = child.left
                # Add to root list
                child.left = self.min_node
                child.right = self.min_node.right
                self.min_node.right.left = child
                self.min_node.right = child
                child.parent = None
                if next_child == min_node.child:
                    break
                child = next_child
        
        # Remove min node from root list
        min_node.left.right = min_node.right
        min_node.right.left = min_node.left
        
        if min_node == min_node.right:
            self.min_node = None
        else:
            self.min_node = min_node.right
            self._consolidate()
        
        self.count -= 1
        return value, min_node.priority

    def decrease_key(self, node, new_priority):
        """
        Decrease the priority of a node.
        
        Args:
            node: The node to modify.
            new_priority: The new priority value.
            
        Returns:
            True if priority was decreased, False otherwise.
        """
        if node is None:
            return False
            
        if new_priority > node.priority:
            return False
            
        node.priority = new_priority
        parent = node.parent
        
        if parent is not None and node.priority < parent.priority:
            self._cut(node, parent)
            self._cascading_cut(parent)
        
        if node.priority < self.min_node.priority:
            self.min_node = node
        
        return True

    def _cut(self, node, parent):
        """Cut a node from its parent and add to root list."""
        # Remove from parent's child list
        if node.left == node:
            parent.child = None
        else:
            node.left.right = node.right
            node.right.left = node.left
            if parent.child == node:
                parent.child = node.left
        
        parent.degree -= 1
        node.parent = None
        node.marked = False
        
        # Add to root list
        node.left = self.min_node
        node.right = self.min_node.right
        self.min_node.right.left = node
        self.min_node.right = node

    def _cascading_cut(self, node):
        """Perform cascading cuts up the tree."""
        parent = node.parent
        if parent is not None:
            if not node.marked:
                node.marked = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)

    def _consolidate(self):
        """Combine trees of the same degree in the root list."""
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
        
        # Find new minimum node
        self.min_node = None
        for node in degree_table:
            if node is not None:
                if self.min_node is None or node.priority < self.min_node.priority:
                    self.min_node = node

    def _link(self, child, parent):
        """Link two trees by making one the child of the other."""
        # Remove child from root list
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
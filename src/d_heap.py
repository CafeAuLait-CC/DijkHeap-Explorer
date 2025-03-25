class DHeap:
    """
    A d-ary heap (d-heap) implementation.
    """
    def __init__(self, num_nodes, num_edges):
        """
        Initialize the d-heap.
        
        :param d: The number of children each node can have (default is 2, which is a binary heap).
        """
        self.heap = []  # List to store the heap elements
        self.d = max(2, num_edges // num_nodes)

    def is_empty(self):
        """Check if the heap is empty."""
        return len(self.heap) == 0

    def push(self, priority, value):
        """
        Insert a value with a given priority into the heap.
        
        :param priority: The priority of the value.
        :param value: The value to insert.
        """
        self.heap.append((priority, value))
        self._bubble_up(len(self.heap) - 1)

    def pop(self):
        """
        Remove and return the value with the smallest priority.
        
        :return: The value with the smallest priority.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty DHeap.")
        
        # Swap the root with the last element
        self._swap(0, len(self.heap) - 1)
        
        # Remove the last element (smallest priority)
        priority, value = self.heap.pop()
        
        # Restore the heap property
        self._bubble_down(0)
        
        return value, priority

    def _bubble_up(self, index):
        """
        Move the element at the given index up to restore the heap property.
        """
        while index > 0:
            parent_index = (index - 1) // self.d
            if self.heap[index][0] < self.heap[parent_index][0]:
                self._swap(index, parent_index)
                index = parent_index
            else:
                break

    def _bubble_down(self, index):
        """
        Move the element at the given index down to restore the heap property.
        """
        while index < len(self.heap):
            smallest_index = index
            # Find the smallest child
            for i in range(1, self.d + 1):
                child_index = self.d * index + i
                if child_index < len(self.heap) and self.heap[child_index][0] < self.heap[smallest_index][0]:
                    smallest_index = child_index
            
            # If the smallest child is smaller than the current node, swap and continue
            if smallest_index != index:
                self._swap(index, smallest_index)
                index = smallest_index
            else:
                break

    def _swap(self, i, j):
        """
        Swap two elements in the heap.
        """
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def __len__(self):
        """Return the number of elements in the heap."""
        return len(self.heap)

    def __str__(self):
        """Return a string representation of the heap."""
        return str(self.heap)
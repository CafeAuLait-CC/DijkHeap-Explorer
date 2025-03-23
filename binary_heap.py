class BinaryHeap:
    """
    A Min Binary Heap implementation.
    """
    def __init__(self):
        self.heap = []  # List to store the heap elements
        self.size = 0   # Number of elements in the heap

    def is_empty(self):
        """Check if the heap is empty."""
        return self.size == 0

    def push(self, priority, value):
        """
        Insert a value with a given priority into the heap.
        
        :param priority: The priority of the value (lower values have higher priority).
        :param value: The value to insert.
        """
        self.heap.append((priority, value))
        self.size += 1
        self._bubble_up(self.size - 1)

    def pop(self):
        """
        Remove and return the value with the smallest priority.
        
        :return: The value with the smallest priority.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty BinaryHeap.")
        
        # Swap the root with the last element
        self._swap(0, self.size - 1)
        
        # Remove the last element (smallest priority)
        priority, value = self.heap.pop()
        self.size -= 1
        
        # Restore the heap property
        self._bubble_down(0)
        
        return value, priority

    def _bubble_up(self, index):
        """
        Move the element at the given index up to restore the heap property.
        """
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index][0] < self.heap[parent_index][0]:
                self._swap(index, parent_index)
                index = parent_index
            else:
                break

    def _bubble_down(self, index):
        """
        Move the element at the given index down to restore the heap property.
        """
        while index < self.size:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            smallest_index = index
            
            # Find the smallest among the current node and its children
            if left_child_index < self.size and self.heap[left_child_index][0] < self.heap[smallest_index][0]:
                smallest_index = left_child_index
            if right_child_index < self.size and self.heap[right_child_index][0] < self.heap[smallest_index][0]:
                smallest_index = right_child_index
            
            # If the smallest is not the current node, swap and continue
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
        return self.size

    def __str__(self):
        """Return a string representation of the heap."""
        return str(self.heap)
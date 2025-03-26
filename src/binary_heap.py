class BinaryHeap:
    """
    A Min Binary Heap implementation with decrease_key support.
    
    Attributes:
        heap: List storing (priority, value) pairs.
        position_map: Dictionary mapping values to their indices in the heap.
        size: Current number of elements in the heap.
    """
    
    def __init__(self):
        """Initialize an empty binary heap."""
        self.heap = []  # List of (priority, value) pairs
        self.position_map = {}  # Maps values to their indices in the heap
        self.size = 0

    def is_empty(self):
        """Check if the heap is empty."""
        return self.size == 0

    def push(self, priority, value):
        """
        Insert a value with given priority into the heap.
        
        Args:
            priority: The priority of the value.
            value: The value to insert.
            
        Note:
            If value already exists, calls decrease_key instead.
        """
        if value in self.position_map:
            return self.decrease_key(value, priority)
            
        self.heap.append((priority, value))
        self.position_map[value] = self.size
        self.size += 1
        self._bubble_up(self.size - 1)

    def pop(self):
        """
        Remove and return the value with the smallest priority.
        
        Returns:
            Tuple of (value, priority) of the minimum element.
            
        Raises:
            IndexError: If the heap is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from empty heap")
            
        self._swap(0, self.size - 1)
        priority, value = self.heap.pop()
        del self.position_map[value]
        self.size -= 1
        
        if not self.is_empty():
            self._bubble_down(0)
            
        return value, priority

    def decrease_key(self, value, new_priority):
        """
        Decrease the priority of an existing value.
        
        Args:
            value: The value to modify.
            new_priority: The new priority value.
            
        Returns:
            True if priority was decreased, False otherwise.
        """
        if value not in self.position_map:
            return False
            
        index = self.position_map[value]
        current_priority = self.heap[index][0]
        
        if new_priority >= current_priority:
            return False
            
        self.heap[index] = (new_priority, value)
        self._bubble_up(index)
        return True

    def contains(self, value):
        """Check if a value exists in the heap."""
        return value in self.position_map

    def _bubble_up(self, index):
        """Move an element up the heap to maintain heap property."""
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[index][0] < self.heap[parent][0]:
                self._swap(index, parent)
                index = parent
            else:
                break

    def _bubble_down(self, index):
        """Move an element down the heap to maintain heap property."""
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index
            
            if left < self.size and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < self.size and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right
                
            if smallest != index:
                self._swap(index, smallest)
                index = smallest
            else:
                break

    def _swap(self, i, j):
        """Swap two elements in the heap and update their positions."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.position_map[self.heap[i][1]] = i
        self.position_map[self.heap[j][1]] = j

    def __len__(self):
        """Return the number of elements in the heap."""
        return self.size
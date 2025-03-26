class DHeap:
    """A d-ary heap implementation with decrease_key support."""
    
    def __init__(self, d=2):
        self.heap = []
        self.d = d  # Branching factor
        self.position_map = {}
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def push(self, priority, value):
        if value in self.position_map:
            return self.decrease_key(value, priority)
            
        self.heap.append((priority, value))
        self.position_map[value] = self.size
        self.size += 1
        self._bubble_up(self.size - 1)

    def pop(self):
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
        return value in self.position_map

    def _bubble_up(self, index):
        while index > 0:
            parent = (index - 1) // self.d
            if self.heap[index][0] < self.heap[parent][0]:
                self._swap(index, parent)
                index = parent
            else:
                break

    def _bubble_down(self, index):
        while True:
            smallest = index
            first_child = self.d * index + 1
            
            for i in range(self.d):
                child = first_child + i
                if child < self.size and self.heap[child][0] < self.heap[smallest][0]:
                    smallest = child
                    
            if smallest != index:
                self._swap(index, smallest)
                index = smallest
            else:
                break

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.position_map[self.heap[i][1]] = i
        self.position_map[self.heap[j][1]] = j

    def __len__(self):
        return self.size
import math

class RadixHeap:
    """Robust Radix Heap implementation with proper position tracking.
    
    Attributes:
        buckets: A list of 65 buckets (0-63 for finite priorities, 64 for infinity).
        min_priority: The current minimum priority in the heap.
        position_map: A dictionary mapping values to their (bucket_idx, position).
        size: The number of elements in the heap.
        last_popped: The priority of the last element popped from the heap.
    """
    
    def __init__(self):
        """Initialize an empty RadixHeap."""
        self.buckets = [[] for _ in range(65)]  # Buckets 0-63 + overflow for infinity
        self.min_priority = None
        self.position_map = {}  # {value: (bucket_idx, position)}
        self.size = 0
        self.last_popped = 0

    def is_empty(self):
        """Check if the heap is empty."""
        return self.size == 0

    def push(self, priority, value):
        """Push a value with given priority into the heap.
        
        Args:
            priority: The priority of the value.
            value: The value to be pushed.
            
        Note:
            If the value already exists, calls decrease_key instead.
            Handles infinity as a special case.
        """
        # Handle existing value
        if value in self.position_map:
            return self.decrease_key(value, priority)
            
        # Handle infinity
        if priority == float('inf'):
            bucket_idx = 64
        else:
            priority = max(priority, self.last_popped)
            diff = priority - self.last_popped
            bucket_idx = min(63, self._get_bucket_idx(diff))
        
        # Add to bucket
        self.buckets[bucket_idx].append((priority, value))
        self.position_map[value] = (bucket_idx, len(self.buckets[bucket_idx])-1)
        self.size += 1
        
        # Update min priority
        if self.min_priority is None or priority < self.min_priority:
            self.min_priority = priority

    def pop(self):
        """Pop the value with minimum priority from the heap.
        
        Returns:
            A tuple of (value, priority) of the minimum element.
            
        Raises:
            IndexError: If the heap is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from empty RadixHeap")
            
        # Find first non-empty bucket
        bucket_idx = 0
        while bucket_idx < 65 and not self.buckets[bucket_idx]:
            bucket_idx += 1
            
        # Find min element in the bucket
        min_idx = 0
        min_priority, min_value = self.buckets[bucket_idx][min_idx]
        for i, (p, v) in enumerate(self.buckets[bucket_idx][1:], 1):
            if p < min_priority:
                min_priority, min_value = p, v
                min_idx = i
                
        # Remove the element
        self._remove_from_bucket(bucket_idx, min_idx)
        self.last_popped = min_priority
        
        # Redistribute remaining elements if needed
        if bucket_idx > 0 and bucket_idx < 64 and self.buckets[bucket_idx]:
            self._redistribute_bucket(bucket_idx)
            
        return min_value, min_priority

    def decrease_key(self, value, new_priority):
        """Decrease the priority of an existing value.
        
        Args:
            value: The value whose priority to decrease.
            new_priority: The new priority.
            
        Returns:
            True if the priority was decreased, False otherwise.
        """
        if value not in self.position_map:
            return False
            
        bucket_idx, pos = self.position_map[value]
        current_priority, _ = self.buckets[bucket_idx][pos]
        
        if new_priority >= current_priority:
            return False
            
        # Remove from current position
        self._remove_from_bucket(bucket_idx, pos)
        
        # Add with new priority
        self.push(new_priority, value)
        return True

    def _remove_from_bucket(self, bucket_idx, pos):
        """Safely remove an element from a bucket and update positions.
        
        Args:
            bucket_idx: Index of the bucket.
            pos: Position within the bucket.
            
        Raises:
            IndexError: If bucket_idx or pos is invalid.
        """
        if not (0 <= bucket_idx < 65) or pos >= len(self.buckets[bucket_idx]):
            raise IndexError("Invalid bucket or position")
            
        # Remove the element
        _, value = self.buckets[bucket_idx][pos]
        del self.position_map[value]
        self.size -= 1
        
        # Swap with last element and pop to avoid shifting
        if pos != len(self.buckets[bucket_idx]) - 1:
            last_val = self.buckets[bucket_idx][-1][1]
            self.buckets[bucket_idx][pos] = self.buckets[bucket_idx][-1]
            self.position_map[last_val] = (bucket_idx, pos)
            
        self.buckets[bucket_idx].pop()

    def _redistribute_bucket(self, bucket_idx):
        """Redistribute elements when their bucket becomes too coarse.
        
        Args:
            bucket_idx: Index of the bucket to redistribute.
        """
        elements = self.buckets[bucket_idx]
        self.buckets[bucket_idx] = []  # Clear the bucket
        
        for priority, value in elements:
            diff = priority - self.last_popped
            new_bucket = min(63, self._get_bucket_idx(diff))
            self.buckets[new_bucket].append((priority, value))
            self.position_map[value] = (new_bucket, len(self.buckets[new_bucket])-1)

    def _get_bucket_idx(self, diff):
        """Calculate bucket index for a given difference.
        
        Args:
            diff: The difference between priority and last_popped.
            
        Returns:
            The appropriate bucket index (0-64).
        """
        if diff <= 0:
            return 0
        if isinstance(diff, int):
            return min(63, diff.bit_length())
        try:
            return min(63, math.floor(math.log2(diff)) + 1)
        except (ValueError, OverflowError):
            return 64

    def __len__(self):
        """Return the number of elements in the heap."""
        return self.size
class RadixHeap:
    """
    A Radix Heap implementation for efficient priority queue operations.
    Assumes that priorities are non-negative integers.
    """
    def __init__(self):
        self.buckets = []  # List of buckets, where each bucket is a list of (priority, value) pairs
        self.min_priority = None  # Tracks the minimum priority in the heap

    def is_empty(self):
        """Check if the heap is empty."""
        return self.min_priority is None

    def push(self, priority, value):
        """
        Insert a value with a given priority into the heap.
        
        :param priority: The priority of the value (must be a non-negative integer).
        :param value: The value to insert.
        """
        if not isinstance(priority, int) or priority < 0:
            raise ValueError("Priority must be a non-negative integer.")
        
        if self.min_priority is None or priority < self.min_priority:
            self.min_priority = priority
        
        # Determine the bucket index based on the binary representation of the priority
        bucket_index = self._get_bucket_index(priority)
        while len(self.buckets) <= bucket_index:
            self.buckets.append([])
        self.buckets[bucket_index].append((priority, value))

    def pop(self):
        """
        Remove and return the value with the smallest priority.
        
        :return: The value with the smallest priority.
        """
        if self.is_empty():
            raise IndexError("Pop from an empty RadixHeap.")
        
        # Find the first non-empty bucket
        bucket_index = 0
        while not self.buckets[bucket_index]:
            bucket_index += 1
        
        # Find the item with the smallest priority in the bucket
        min_index = 0
        for i in range(1, len(self.buckets[bucket_index])):
            if self.buckets[bucket_index][i][0] < self.buckets[bucket_index][min_index][0]:
                min_index = i
        
        # Remove and return the item
        priority, value = self.buckets[bucket_index].pop(min_index)
        
        # Update the minimum priority
        self.min_priority = None
        for bucket in self.buckets:
            if bucket:
                if self.min_priority is None:
                    self.min_priority = bucket[0][0]
                else:
                    self.min_priority = min(self.min_priority, bucket[0][0])
        
        return value, priority  # Return both the value and its priority

    def _get_bucket_index(self, priority):
        """
        Determine the bucket index for a given priority.
        
        :param priority: The priority of the item.
        :return: The index of the bucket.
        """
        if priority == 0:
            return 0
        return (priority.bit_length() - 1)

    def __len__(self):
        """Return the number of items in the heap."""
        return sum(len(bucket) for bucket in self.buckets)

    def __str__(self):
        """Return a string representation of the heap."""
        return "\n".join(f"Bucket {i}: {bucket}" for i, bucket in enumerate(self.buckets))
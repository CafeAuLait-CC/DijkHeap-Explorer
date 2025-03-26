import unittest
from src.fibonacci_heap import FibonacciHeap

class TestFibonacciHeap(unittest.TestCase):
    def setUp(self):
        self.heap = FibonacciHeap()

    def test_empty_heap(self):
        self.assertTrue(self.heap.is_empty())
        self.assertEqual(len(self.heap), 0)
        with self.assertRaises(IndexError):
            self.heap.pop()

    def test_basic_operations(self):
        self.heap.push(3, 'A')
        self.heap.push(1, 'B')
        self.heap.push(2, 'C')
        
        self.assertEqual(len(self.heap), 3)
        self.assertEqual(self.heap.pop(), ('B', 1))
        self.assertEqual(self.heap.pop(), ('C', 2))
        self.assertEqual(self.heap.pop(), ('A', 3))
        self.assertTrue(self.heap.is_empty())

    def test_decrease_key(self):
        # Push items and keep node references
        node_a = self.heap.push(5, 'A')
        node_b = self.heap.push(10, 'B')
        node_c = self.heap.push(15, 'C')
        
        # Need to get the actual node objects for decrease_key
        # In the current implementation, push doesn't return nodes
        # So we need to modify either the test or the FibonacciHeap
        
        # Option 1: Modify FibonacciHeap.push() to return the node
        # (Change push() to return new_node)
        
        # Option 2: For testing, get nodes from the root list
        current = self.heap.min_node
        nodes = []
        while True:
            nodes.append(current)
            current = current.right
            if current == self.heap.min_node:
                break
        
        # Now we can test decrease_key properly
        # Find node_b (priority 10)
        node_to_decrease = next(n for n in nodes if n.priority == 10)
        self.assertTrue(self.heap.decrease_key(node_to_decrease, 2))
        
        # Verify the heap structure
        self.assertEqual(self.heap.min_node.priority, 2)

    def test_large_heap(self):
        for i in range(100, 0, -1):
            self.heap.push(i, str(i))
        
        self.assertEqual(len(self.heap), 100)
        
        for expected in range(1, 101):
            value, priority = self.heap.pop()
            self.assertEqual(priority, expected)
            self.assertEqual(value, str(expected))

    def test_consolidation(self):
        # Test that consolidation works properly
        for i in range(1, 11):  # Push numbers 1-10
            self.heap.push(i, i)  # Use same value for priority and value
        
        # Pop all items to trigger consolidation
        results = []
        while not self.heap.is_empty():
            results.append(self.heap.pop()[0])  # Get the value
        
        self.assertEqual(results, list(range(1, 11)))

    def test_duplicate_priorities(self):
        self.heap.push(1, 'A')
        self.heap.push(1, 'B')
        self.heap.push(1, 'C')
        
        # All have same priority, any order is acceptable
        values = set()
        while not self.heap.is_empty():
            values.add(self.heap.pop()[0])
        
        self.assertEqual(values, {'A', 'B', 'C'})

if __name__ == '__main__':
    unittest.main()
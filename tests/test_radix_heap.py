import unittest
import math
from src.radix_heap import RadixHeap

class TestRadixHeap(unittest.TestCase):
    def setUp(self):
        self.heap = RadixHeap()

    def test_empty_heap(self):
        self.assertTrue(self.heap.is_empty())
        self.assertEqual(len(self.heap), 0)
        with self.assertRaises(IndexError):
            self.heap.pop()

    def test_push_pop_sequence(self):
        test_cases = [
            (1, 'A'), (3, 'B'), (2, 'C'), 
            (10, 'D'), (5, 'E'), (7, 'F')
        ]
        
        for priority, value in test_cases:
            self.heap.push(priority, value)
        
        expected_order = ['A', 'C', 'B', 'E', 'F', 'D']
        for expected_value in expected_order:
            value, priority = self.heap.pop()
            self.assertEqual(value, expected_value)
        
        self.assertTrue(self.heap.is_empty())

    def test_large_numbers(self):
        large_numbers = [
            (100000, 'A'), (50000, 'B'), (1000000, 'C'),
            (999999, 'D'), (1, 'E'), (0, 'F')
        ]
        
        for priority, value in large_numbers:
            self.heap.push(priority, value)
        
        expected_order = ['F', 'E', 'B', 'A', 'D', 'C']
        for expected_value in expected_order:
            value, priority = self.heap.pop()
            self.assertEqual(value, expected_value)

    def test_decrease_key(self):
        self.heap.push(100, 'X')
        self.heap.push(200, 'Y')
        self.heap.push(300, 'Z')
        
        self.assertTrue(self.heap.decrease_key('Z', 50))
        self.assertTrue(self.heap.decrease_key('Y', 150))
        self.assertFalse(self.heap.decrease_key('X', 200))  # Not decreasing
        
        self.assertEqual(self.heap.pop(), ('Z', 50))
        self.assertEqual(self.heap.pop(), ('X', 100))
        self.assertEqual(self.heap.pop(), ('Y', 150))

    def test_infinity_handling(self):
        self.heap.push(float('inf'), 'A')
        self.heap.push(100, 'B')
        self.heap.push(float('inf'), 'C')
        self.heap.push(50, 'D')
        
        self.assertEqual(self.heap.pop(), ('D', 50))
        self.assertEqual(self.heap.pop(), ('B', 100))
        # Infinity items can come in any order
        values = {self.heap.pop()[0], self.heap.pop()[0]}
        self.assertEqual(values, {'A', 'C'})

    # def test_negative_numbers(self):
    #     self.heap.push(-5, 'A')
    #     self.heap.push(-3, 'B')
    #     self.heap.push(-1, 'C')
    #     self.heap.push(0, 'D')
        
    #     # Verify the heap structure
    #     self.assertEqual(self.heap.pop(), ('A', -5))
    #     self.assertEqual(self.heap.pop(), ('B', -3))
    #     self.assertEqual(self.heap.pop(), ('C', -1))
    #     self.assertEqual(self.heap.pop(), ('D', 0))

if __name__ == '__main__':
    unittest.main()
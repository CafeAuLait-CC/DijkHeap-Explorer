import unittest
from src.binary_heap import BinaryHeap

class TestBinaryHeap(unittest.TestCase):
    def setUp(self):
        self.heap = BinaryHeap()

    def test_empty_heap(self):
        self.assertTrue(self.heap.is_empty())
        self.assertEqual(len(self.heap), 0)
        with self.assertRaises(IndexError):
            self.heap.pop()

    def test_push_and_pop(self):
        self.heap.push(3, 'A')
        self.heap.push(1, 'B')
        self.heap.push(2, 'C')
        
        self.assertFalse(self.heap.is_empty())
        self.assertEqual(len(self.heap), 3)
        
        # Should return items in priority order
        self.assertEqual(self.heap.pop(), ('B', 1))
        self.assertEqual(self.heap.pop(), ('C', 2))
        self.assertEqual(self.heap.pop(), ('A', 3))
        self.assertTrue(self.heap.is_empty())

    def test_decrease_key(self):
        self.heap.push(3, 'A')
        self.heap.push(5, 'B')
        self.heap.push(10, 'C')
        
        # Decrease priority of 'C' from 10 to 1
        self.assertTrue(self.heap.decrease_key('C', 1))
        self.assertEqual(self.heap.pop(), ('C', 1))
        
        # Try to increase priority (should fail)
        self.assertFalse(self.heap.decrease_key('B', 6))
        
        # Decrease priority of 'B' from 5 to 2
        self.assertTrue(self.heap.decrease_key('B', 2))
        self.assertEqual(self.heap.pop(), ('B', 2))
        self.assertEqual(self.heap.pop(), ('A', 3))

    def test_contains(self):
        self.heap.push(2, 'X')
        self.heap.push(1, 'Y')
        
        self.assertTrue(self.heap.contains('X'))
        self.assertTrue(self.heap.contains('Y'))
        self.assertFalse(self.heap.contains('Z'))

if __name__ == '__main__':
    unittest.main()
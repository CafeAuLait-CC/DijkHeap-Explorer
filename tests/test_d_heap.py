import unittest
from src.d_heap import DHeap

class TestDHeap(unittest.TestCase):
    def test_different_d_values(self):
        for d in [2, 3, 4, 5]:
            with self.subTest(d=d):
                heap = DHeap(d=d)
                heap.push(3, 'A')
                heap.push(1, 'B')
                heap.push(2, 'C')
                heap.push(4, 'D')
                
                self.assertEqual(heap.pop(), ('B', 1))
                self.assertEqual(heap.pop(), ('C', 2))
                self.assertEqual(heap.pop(), ('A', 3))
                self.assertEqual(heap.pop(), ('D', 4))

    def test_large_d_heap(self):
        heap = DHeap(d=10)
        items = [(i, str(i)) for i in range(100, 0, -1)]
        
        for priority, value in items:
            heap.push(priority, value)
        
        for expected in range(1, 101):
            value, priority = heap.pop()
            self.assertEqual(priority, expected)
            self.assertEqual(value, str(expected))

    # Inherit other tests from BinaryHeap since interface is similar
    def test_empty_heap(self):
        heap = DHeap(d=3)
        self.assertTrue(heap.is_empty())
        self.assertEqual(len(heap), 0)
        with self.assertRaises(IndexError):
            heap.pop()

    def test_decrease_key(self):
        heap = DHeap(d=4)
        heap.push(3, 'A')
        heap.push(5, 'B')
        heap.push(10, 'C')
        
        self.assertTrue(heap.decrease_key('C', 1))
        self.assertEqual(heap.pop(), ('C', 1))
        self.assertFalse(heap.decrease_key('B', 6))
        self.assertTrue(heap.decrease_key('B', 2))
        self.assertEqual(heap.pop(), ('B', 2))
        self.assertEqual(heap.pop(), ('A', 3))

if __name__ == '__main__':
    unittest.main()
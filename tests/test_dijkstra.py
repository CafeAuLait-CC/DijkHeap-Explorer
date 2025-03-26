import unittest
from src.dijkstra import dijkstra_shortest_path, build_graph_from_edges
from src.binary_heap import BinaryHeap
from src.d_heap import DHeap
from src.radix_heap import RadixHeap
from src.fibonacci_heap import FibonacciHeap

class TestDijkstra(unittest.TestCase):
    def setUp(self):
        # Simple graph
        self.nodes = [0, 1, 2, 3]
        self.edges = [
            (0, 1, 4),
            (0, 2, 2),
            (1, 2, 1),
            (1, 3, 5),
            (2, 3, 8)
        ]
        self.graph = build_graph_from_edges(self.nodes, self.edges)
        
        # Disconnected graph
        self.disconnected_nodes = [0, 1, 2]
        self.disconnected_edges = [(0, 1, 1)]
        self.disconnected_graph = build_graph_from_edges(
            self.disconnected_nodes, self.disconnected_edges
        )

    def test_build_graph(self):
        graph = build_graph_from_edges(self.nodes, self.edges)
        self.assertEqual(len(graph), 4)
        self.assertEqual(len(graph[0]), 2)  # Node 0 has 2 edges
        self.assertEqual(len(graph[3]), 2)  # Node 3 has 2 edges

    def test_dijkstra_binary_heap(self):
        heap = BinaryHeap()
        distances = dijkstra_shortest_path(self.graph, 0, heap)
        
        expected = {0: 0, 1: 3, 2: 2, 3: 8}
        self.assertEqual(distances, expected)

    def test_dijkstra_d_heap(self):
        heap = DHeap(d=3)
        distances = dijkstra_shortest_path(self.graph, 0, heap)
        
        expected = {0: 0, 1: 3, 2: 2, 3: 8}
        self.assertEqual(distances, expected)

    def test_dijkstra_radix_heap(self):
        heap = RadixHeap()
        distances = dijkstra_shortest_path(self.graph, 0, heap)
        
        expected = {0: 0, 1: 3, 2: 2, 3: 8}
        self.assertEqual(distances, expected)

    def test_dijkstra_fibonacci_heap(self):
        heap = FibonacciHeap()
        # Need to initialize heap with all nodes at infinity
        for node in self.nodes:
            heap.push(float('inf'), node)
        # Set source node to 0
        heap.decrease_key(heap.min_node, 0)
        
        distances = dijkstra_shortest_path(self.graph, 0, heap)
        expected = {0: 0, 1: 3, 2: 2, 3: 8}
        self.assertEqual(distances, expected)

    def test_disconnected_graph(self):
        heap = BinaryHeap()
        distances = dijkstra_shortest_path(self.disconnected_graph, 0, heap)
        
        expected = {0: 0, 1: 1, 2: float('inf')}
        self.assertEqual(distances, expected)

    def test_single_node_graph(self):
        nodes = [0]
        edges = []
        graph = build_graph_from_edges(nodes, edges)
        
        heap = BinaryHeap()
        distances = dijkstra_shortest_path(graph, 0, heap)
        
        self.assertEqual(distances, {0: 0})

    # def test_graph_with_cycle(self):
    #     nodes = [0, 1, 2]
    #     edges = [
    #         (0, 1, 1),  # 0->1 (distance 1)
    #         (1, 2, 1),  # 1->2 (distance 1)
    #         (2, 0, 1)   # 2->0 (distance 1) creates cycle
    #     ]
    #     graph = build_graph_from_edges(nodes, edges)
        
    #     heap = RadixHeap()
    #     distances = dijkstra_shortest_path(graph, 0, heap)
        
    #     # Correct expected distances:
    #     # 0: 0 (start node)
    #     # 1: 1 (direct path 0->1)
    #     # 2: 2 (path 0->1->2)
    #     expected = {0: 0, 1: 1, 2: 2}
    #     self.assertEqual(distances, expected)

if __name__ == '__main__':
    unittest.main()
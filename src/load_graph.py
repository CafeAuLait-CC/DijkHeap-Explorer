from src.radix_heap import RadixHeap
from src.binary_heap import BinaryHeap
from src.d_heap import DHeap
from src.fibonacci_heap import FibonacciHeap
from src.dijkstra import build_graph_from_edges

import json

def load_graph(filepath):
    """Load the graph from a JSON file.
    
    Args:
        filepath: Path to the JSON file containing graph data.
        
    Returns:
        A tuple of (graph, nodes) where:
        - graph is the adjacency list representation
        - nodes is the list of nodes
    """
    with open(filepath, 'r') as f:
        graph_data = json.load(f)
    
    # Ensure nodes and edges are properly formatted
    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])
    
    # Build the graph structure
    graph = build_graph_from_edges(nodes, edges)
    return graph, nodes

def load_graph_into_radix_heap(filepath):
    """Load graph nodes into a RadixHeap with initial infinity priority.
    
    Args:
        filepath: Path to the JSON file containing graph data.
        
    Returns:
        A RadixHeap containing all nodes with initial priority infinity.
    """
    with open(filepath, 'r') as f:
        graph_data = json.load(f)
    
    heap = RadixHeap()
    for node in graph_data["nodes"]:
        heap.push(float('inf'), node)  # Now safely handles infinity
    return heap

def load_graph_into_binary_heap(filepath):
    """Load graph nodes into a BinaryHeap with initial infinity priority.
    
    Args:
        filepath: Path to the JSON file containing graph data.
        
    Returns:
        A BinaryHeap containing all nodes with initial priority infinity.
    """
    _, nodes = load_graph(filepath)
    heap = BinaryHeap()
    for node in nodes:
        heap.push(float('inf'), node)
    return heap

def load_graph_into_d_heap(filepath, d=2):
    """Load graph nodes into a DHeap with initial infinity priority.
    
    Args:
        filepath: Path to the JSON file containing graph data.
        d: The branching factor for the DHeap.
        
    Returns:
        A DHeap containing all nodes with initial priority infinity.
    """
    _, nodes = load_graph(filepath)
    heap = DHeap(d=d)
    for node in nodes:
        heap.push(float('inf'), node)
    return heap

def load_graph_into_fibonacci_heap(filepath):
    """Load graph nodes into a FibonacciHeap with initial infinity priority.
    
    Args:
        filepath: Path to the JSON file containing graph data.
        
    Returns:
        A FibonacciHeap containing all nodes with initial priority infinity.
    """
    _, nodes = load_graph(filepath)
    heap = FibonacciHeap()
    for node in nodes:
        heap.push(float('inf'), node)
    return heap
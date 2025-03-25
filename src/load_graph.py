from src.radix_heap import RadixHeap
from src.binary_heap import BinaryHeap
from src.d_heap import DHeap
from src.fibonacci_heap import FibonacciHeap
from src.dijkstra import build_graph_from_edges

import json

def load_graph_into_radix_heap(filepath):
    """
    Load a graph from a JSON file and insert its nodes into a RadixHeap.
    
    :param filepath: Path to the JSON file.
    :return: A RadixHeap containing the graph's nodes.
    """
    with open(filepath, 'r') as f:
        graph_data = json.load(f)
    
    radix_heap = RadixHeap()
    for node in graph_data["nodes"]:
        radix_heap.push(10**18, node)  # Initialize all nodes with infinite distance
    return radix_heap

def load_graph_into_binary_heap(filepath):
    """
    Load a graph from a JSON file and insert its nodes into a BinaryHeap.
    
    :param filepath: Path to the JSON file.
    :return: A BinaryHeap containing the graph's nodes.
    """
    with open(filepath, 'r') as f:
        graph_data = json.load(f)
    
    binary_heap = BinaryHeap()
    for node in graph_data["nodes"]:
        binary_heap.push(float('inf'), node)  # Initialize all nodes with infinite distance
    return binary_heap

def load_graph_into_d_heap(filepath):
    """
    Load a graph from a JSON file and insert its nodes into a DHeap.
    
    :param filepath: Path to the JSON file.
    :param d: The number of children per node in the DHeap (default is 4).
    :return: A DHeap containing the graph's nodes.
    """
    with open(filepath, 'r') as f:
        graph_data = json.load(f)
    
    d_heap = DHeap(num_nodes=len(graph_data["nodes"]), num_edges = len(graph_data["edges"])) 
    for node in graph_data["nodes"]:
        d_heap.push(10**18, node)  # Use a large integer instead of infinity
    return d_heap

def load_graph_into_fibonacci_heap(filepath):
    """
    Load a graph from a JSON file and insert its nodes into a FibonacciHeap.
    
    :param filepath: Path to the JSON file.
    :return: A FibonacciHeap containing the graph's nodes.
    """
    with open(filepath, 'r') as f:
        graph_data = json.load(f)
    
    fibonacci_heap = FibonacciHeap()
    for node in graph_data["nodes"]:
        fibonacci_heap.push(10**18, node)  # Use a large integer instead of infinity
    return fibonacci_heap

def load_graph(filepath):
    """
    Load the graph from a JSON file and build the graph representation.
    
    :param filepath: Path to the JSON file.
    :return: A tuple containing the graph and the list of nodes.
    """
    print(f"Loading graph from {filepath}...")
    with open(filepath, 'r') as f:
        graph_data = json.load(f)
    
    print("Building graph from edges...")
    graph = build_graph_from_edges(graph_data["nodes"], graph_data["edges"])
    
    return graph, graph_data["nodes"]

import json
import time
import csv
from radix_heap import RadixHeap
from binary_heap import BinaryHeap
from d_heap import DHeap
from fibonacci_heap import FibonacciHeap
from dijkstra import dijkstra_shortest_path, build_graph_from_edges
import matplotlib.pyplot as plt

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

def load_graph_into_d_heap(filepath, d=4):
    """
    Load a graph from a JSON file and insert its nodes into a DHeap.
    
    :param filepath: Path to the JSON file.
    :param d: The number of children per node in the DHeap (default is 4).
    :return: A DHeap containing the graph's nodes.
    """
    with open(filepath, 'r') as f:
        graph_data = json.load(f)
    
    d_heap = DHeap(d=d)
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

def run_dijkstra(graph, source_node, heap, heap_type):
    """
    Run Dijkstra's algorithm using the given heap and measure the time consumed.
    
    :param graph: The graph representation.
    :param source_node: The source node for Dijkstra's algorithm.
    :param heap: The heap object (RadixHeap or BinaryHeap).
    :param heap_type: A string describing the heap type (for logging).
    :return: A dictionary containing the shortest distances from the source node.
    """
    print(f"\nRunning Dijkstra's algorithm with {heap_type} from source node {source_node}...")
    
    # Initialize the source node distance to 0
    heap.push(0, source_node)
    
    start_time = time.time()  # Start timing
    shortest_distances = dijkstra_shortest_path(graph, source_node, heap)
    end_time = time.time()  # End timing
    
    time_consumed = end_time - start_time
    print(f"\nTime consumed by Dijkstra's algorithm ({heap_type}): {time_consumed:.6f} seconds")
    
    return shortest_distances

def print_shortest_distances(shortest_distances, heap_type):
    """
    Print the shortest distances from the source node in a compact format.
    
    :param shortest_distances: A dictionary containing the shortest distances.
    :param heap_type: A string describing the heap type (for logging).
    """
    print(f"\nShortest distances from source node ({heap_type}):")
    
    # Extract distances and sort them
    distances = list(shortest_distances.values())
    distances.sort()
    
    # Print the first 5 and last 5 distances
    print("First 5 distances:", distances[:5])
    print("Last 5 distances:", distances[-5:])
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Total nodes: {len(shortest_distances)}")
    print(f"Minimum distance: {min(distances)}")
    print(f"Maximum distance: {max(distances)}")
    print(f"Average distance: {sum(distances) / len(distances):.2f}")

def run_experiment(data_file, graph_size):
    """
    Run Dijkstra's algorithm on the given graph and record the time consumed.
    
    :param data_file: Path to the graph file.
    :param graph_size: Size of the graph (number of nodes).
    :return: A tuple containing the time consumed by RadixHeap, BinaryHeap, DHeap, and FibonacciHeap.
    """
    # Load and build the graph
    graph, nodes = load_graph(data_file)
    
    # Define the source node
    source_node = 0
    
    # Run Dijkstra's algorithm with RadixHeap
    radix_heap = load_graph_into_radix_heap(data_file)
    start_time = time.time()
    _ = run_dijkstra(graph, source_node, radix_heap, "RadixHeap")
    radix_time = time.time() - start_time
    
    # Run Dijkstra's algorithm with BinaryHeap
    binary_heap = load_graph_into_binary_heap(data_file)
    start_time = time.time()
    _ = run_dijkstra(graph, source_node, binary_heap, "BinaryHeap")
    binary_time = time.time() - start_time
    
    # Run Dijkstra's algorithm with DHeap
    d_heap = load_graph_into_d_heap(data_file, d=4)  # Use d=4 for a 4-ary heap
    start_time = time.time()
    _ = run_dijkstra(graph, source_node, d_heap, "DHeap")
    d_heap_time = time.time() - start_time
    
    # Run Dijkstra's algorithm with FibonacciHeap
    fibonacci_heap = load_graph_into_fibonacci_heap(data_file)
    start_time = time.time()
    _ = run_dijkstra(graph, source_node, fibonacci_heap, "FibonacciHeap")
    fibonacci_time = time.time() - start_time
    
    return radix_time, binary_time, d_heap_time, fibonacci_time

def save_results_to_csv(results, filename):
    """
    Save the experiment results to a CSV file.
    
    :param results: A list of tuples (graph_size, radix_time, binary_time, d_heap_time, fibonacci_time).
    :param filename: The name of the CSV file.
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Graph Size", "RadixHeap Time (s)", "BinaryHeap Time (s)", "DHeap Time (s)", "FibonacciHeap Time (s)"])
        writer.writerows(results)
    
    print(f"Results saved to {filename}")

def plot_results(results):
    """
    Plot the experiment results.
    
    :param results: A list of tuples (graph_size, radix_time, binary_time, d_heap_time, fibonacci_time).
    """
    graph_sizes = [result[0] for result in results]
    radix_times = [result[1] for result in results]
    binary_times = [result[2] for result in results]
    d_heap_times = [result[3] for result in results]
    fibonacci_times = [result[4] for result in results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(graph_sizes, radix_times, marker='o', label="RadixHeap")
    plt.plot(graph_sizes, binary_times, marker='o', label="BinaryHeap")
    plt.plot(graph_sizes, d_heap_times, marker='o', label="DHeap (d=4)")
    plt.plot(graph_sizes, fibonacci_times, marker='o', label="FibonacciHeap")
    
    plt.xlabel("Graph Size (Number of Nodes)")
    plt.ylabel("Time Consumed (Seconds)")
    plt.title("Dijkstra's Algorithm Performance: RadixHeap vs BinaryHeap vs DHeap vs FibonacciHeap")
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage
if __name__ == "__main__":
    # # Load the graph into a RadixHeap
    # radix_heap = load_graph_into_radix_heap("data/graph_example.json")
    
    # # Print the RadixHeap
    # print("Radix Heap Contents:")
    # while not radix_heap.is_empty():
    #     edge, weight = radix_heap.pop()  # Get both the edge and its weight
    #     print(f"Edge {edge} with weight {weight}")

     # Load the graph into a BinaryHeap
    data_file = "data/graph_example.json"
    print(f"Loading graph from {data_file}...")
    binary_heap = load_graph_into_binary_heap(data_file)
    
    # Print the BinaryHeap contents
    print("Binary Heap Contents:")
    while not binary_heap.is_empty():
        edge, weight = binary_heap.pop()
        print(f"Edge {edge} with weight {weight}")
import csv
import json
import os, time
import tracemalloc

import matplotlib.pyplot as plt

from src.radix_heap import RadixHeap
from src.binary_heap import BinaryHeap
from src.d_heap import DHeap
from src.fibonacci_heap import FibonacciHeap
from src.dijkstra import dijkstra_shortest_path, build_graph_from_edges


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

def get_available_datasets():
    """
    Scan the /data folder for all JSON files and return their paths and sizes.
    
    :return: A list of tuples (filepath, graph_size).
    """
    datasets = []
    data_dir = "data"
    if not os.path.exists(data_dir):
        print(f"Directory '{data_dir}' does not exist. Please generate datasets first.")
        return datasets
    
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'r') as f:
                graph_data = json.load(f)
            graph_size = len(graph_data["nodes"])
            datasets.append((filepath, graph_size))
    
    return datasets

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
    Run Dijkstra's algorithm on the given graph and record the time and memory consumed.
    
    :param data_file: Path to the graph file.
    :param graph_size: Size of the graph (number of nodes).
    :return: A tuple containing the time and memory consumed by RadixHeap, BinaryHeap, DHeap, and FibonacciHeap.
    """
    # Load and build the graph
    graph, nodes = load_graph(data_file)
    
    # Define the source node
    source_node = 0
    
    # Run Dijkstra's algorithm with RadixHeap
    tracemalloc.start()
    radix_heap = load_graph_into_radix_heap(data_file)
    start_time = time.time()
    _ = run_dijkstra(graph, source_node, radix_heap, "RadixHeap")
    radix_time = time.time() - start_time
    radix_memory = tracemalloc.get_traced_memory()[1]  # Peak memory usage
    tracemalloc.stop()
    
    # Run Dijkstra's algorithm with BinaryHeap
    tracemalloc.start()
    binary_heap = load_graph_into_binary_heap(data_file)
    start_time = time.time()
    _ = run_dijkstra(graph, source_node, binary_heap, "BinaryHeap")
    binary_time = time.time() - start_time
    binary_memory = tracemalloc.get_traced_memory()[1]  # Peak memory usage
    tracemalloc.stop()
    
    # Run Dijkstra's algorithm with DHeap
    tracemalloc.start()
    d_heap = load_graph_into_d_heap(data_file, d=4)  # Use d=4 for a 4-ary heap
    start_time = time.time()
    _ = run_dijkstra(graph, source_node, d_heap, "DHeap")
    d_heap_time = time.time() - start_time
    d_heap_memory = tracemalloc.get_traced_memory()[1]  # Peak memory usage
    tracemalloc.stop()
    
    # Run Dijkstra's algorithm with FibonacciHeap
    tracemalloc.start()
    fibonacci_heap = load_graph_into_fibonacci_heap(data_file)
    start_time = time.time()
    _ = run_dijkstra(graph, source_node, fibonacci_heap, "FibonacciHeap")
    fibonacci_time = time.time() - start_time
    fibonacci_memory = tracemalloc.get_traced_memory()[1]  # Peak memory usage
    tracemalloc.stop()
    
    return (
        (radix_time, radix_memory),
        (binary_time, binary_memory),
        (d_heap_time, d_heap_memory),
        (fibonacci_time, fibonacci_memory)
    )

def save_results_to_csv(results, filename):
    """
    Save the experiment results to a CSV file.
    
    :param results: A list of tuples (graph_size, radix_time, radix_memory, binary_time, binary_memory, d_heap_time, d_heap_memory, fibonacci_time, fibonacci_memory).
    :param filename: The name of the CSV file.
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Graph Size", 
            "RadixHeap Time (s)", "RadixHeap Memory (B)", 
            "BinaryHeap Time (s)", "BinaryHeap Memory (B)", 
            "DHeap Time (s)", "DHeap Memory (B)", 
            "FibonacciHeap Time (s)", "FibonacciHeap Memory (B)"
        ])
        writer.writerows(results)
    
    print(f"Results saved to {filename}")

def plot_results(results):
    """
    Plot the experiment results by averaging datapoints with the same dataset and heap type.
    
    :param results: A list of tuples (graph_size, radix_time, radix_memory, binary_time, binary_memory, d_heap_time, d_heap_memory, fibonacci_time, fibonacci_memory).
    """
    from collections import defaultdict

    # Group results by graph size
    grouped_results = defaultdict(lambda: {
        "radix_times": [],
        "radix_memory": [],
        "binary_times": [],
        "binary_memory": [],
        "d_heap_times": [],
        "d_heap_memory": [],
        "fibonacci_times": [],
        "fibonacci_memory": []
    })

    for result in results:
        graph_size = result[0]
        grouped_results[graph_size]["radix_times"].append(result[1][0])
        grouped_results[graph_size]["radix_memory"].append(result[1][1])
        grouped_results[graph_size]["binary_times"].append(result[2][0])
        grouped_results[graph_size]["binary_memory"].append(result[2][1])
        grouped_results[graph_size]["d_heap_times"].append(result[3][0])
        grouped_results[graph_size]["d_heap_memory"].append(result[3][1])
        grouped_results[graph_size]["fibonacci_times"].append(result[4][0])
        grouped_results[graph_size]["fibonacci_memory"].append(result[4][1])

    # Calculate averages
    graph_sizes = sorted(grouped_results.keys())
    radix_times_avg = [sum(grouped_results[size]["radix_times"]) / len(grouped_results[size]["radix_times"]) for size in graph_sizes]
    radix_memory_avg = [sum(grouped_results[size]["radix_memory"]) / len(grouped_results[size]["radix_memory"]) for size in graph_sizes]
    binary_times_avg = [sum(grouped_results[size]["binary_times"]) / len(grouped_results[size]["binary_times"]) for size in graph_sizes]
    binary_memory_avg = [sum(grouped_results[size]["binary_memory"]) / len(grouped_results[size]["binary_memory"]) for size in graph_sizes]
    d_heap_times_avg = [sum(grouped_results[size]["d_heap_times"]) / len(grouped_results[size]["d_heap_times"]) for size in graph_sizes]
    d_heap_memory_avg = [sum(grouped_results[size]["d_heap_memory"]) / len(grouped_results[size]["d_heap_memory"]) for size in graph_sizes]
    fibonacci_times_avg = [sum(grouped_results[size]["fibonacci_times"]) / len(grouped_results[size]["fibonacci_times"]) for size in graph_sizes]
    fibonacci_memory_avg = [sum(grouped_results[size]["fibonacci_memory"]) / len(grouped_results[size]["fibonacci_memory"]) for size in graph_sizes]

    # Plot time comparison
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(graph_sizes, radix_times_avg, marker='o', label="RadixHeap")
    plt.plot(graph_sizes, binary_times_avg, marker='o', label="BinaryHeap")
    plt.plot(graph_sizes, d_heap_times_avg, marker='o', label="DHeap (d=4)")
    plt.plot(graph_sizes, fibonacci_times_avg, marker='o', label="FibonacciHeap")
    plt.xlabel("Graph Size (Number of Nodes)")
    plt.ylabel("Average Time Consumed (Seconds)")
    plt.title("Time Comparison (Averaged)")
    plt.legend()
    plt.grid(True)
    
    # Plot memory comparison as a bar chart
    plt.subplot(1, 2, 2)
    bar_width = 0.2
    x = range(len(graph_sizes))
    plt.bar([i - 1.5 * bar_width for i in x], radix_memory_avg, width=bar_width, label="RadixHeap")
    plt.bar([i - 0.5 * bar_width for i in x], binary_memory_avg, width=bar_width, label="BinaryHeap")
    plt.bar([i + 0.5 * bar_width for i in x], d_heap_memory_avg, width=bar_width, label="DHeap (d=4)")
    plt.bar([i + 1.5 * bar_width for i in x], fibonacci_memory_avg, width=bar_width, label="FibonacciHeap")
    plt.xticks(x, graph_sizes)
    plt.xlabel("Graph Size (Number of Nodes)")
    plt.ylabel("Average Memory Consumed (Bytes)")
    plt.title("Memory Comparison (Averaged)")
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
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
import csv
import time
import matplotlib.pyplot as plt
from helper import load_graph_into_radix_heap, load_graph_into_binary_heap
from helper import load_graph, run_dijkstra, print_shortest_distances

def run_experiment(data_file, graph_size):
    """
    Run Dijkstra's algorithm on the given graph and record the time consumed.
    
    :param data_file: Path to the graph file.
    :param graph_size: Size of the graph (number of nodes).
    :return: A tuple containing the time consumed by RadixHeap and BinaryHeap.
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
    
    return radix_time, binary_time

def save_results_to_csv(results, filename):
    """
    Save the experiment results to a CSV file.
    
    :param results: A list of tuples (graph_size, radix_time, binary_time).
    :param filename: The name of the CSV file.
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Graph Size", "RadixHeap Time (s)", "BinaryHeap Time (s)"])
        writer.writerows(results)
    
    print(f"Results saved to {filename}")

def plot_results(results):
    """
    Plot the experiment results.
    
    :param results: A list of tuples (graph_size, radix_time, binary_time).
    """
    graph_sizes = [result[0] for result in results]
    radix_times = [result[1] for result in results]
    binary_times = [result[2] for result in results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(graph_sizes, radix_times, marker='o', label="RadixHeap")
    plt.plot(graph_sizes, binary_times, marker='o', label="BinaryHeap")
    
    plt.xlabel("Graph Size (Number of Nodes)")
    plt.ylabel("Time Consumed (Seconds)")
    plt.title("Dijkstra's Algorithm Performance: RadixHeap vs BinaryHeap")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    # Define the graph files and their sizes
    experiments = [
        ("data/graph_example.json", 10),  # Small graph
        ("data/large_graph.json", 100)    # Large graph
    ]
    
    # Run experiments and record results
    results = []
    for data_file, graph_size in experiments:
        print(f"\nRunning experiment on graph: {data_file} (Size: {graph_size})")
        radix_time, binary_time = run_experiment(data_file, graph_size)
        results.append((graph_size, radix_time, binary_time))
    
    # Save results to CSV
    save_results_to_csv(results, "results.csv")
    
    # Plot results
    plot_results(results)

if __name__ == "__main__":
    main()
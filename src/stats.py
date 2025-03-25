import csv, os
from src.helper import Colors
from collections import defaultdict
import matplotlib.pyplot as plt

def save_results_to_csv(results, filename):
    """
    Save the experiment results to a CSV file.
    
    :param results: A list of tuples (graph_size, radix_time, radix_memory, binary_time, binary_memory, d_heap_time, d_heap_memory, fibonacci_time, fibonacci_memory).
    :param filename: The name of the CSV file.
    """
    result_dir = "results"
    filename = filename + ".csv"
    filename = os.path.join(result_dir, filename)
    os.makedirs(result_dir, exist_ok=True)
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Graph Size", 
            "Graph Type",
            "RadixHeap Time (s)", "RadixHeap Memory (B)", 
            "BinaryHeap Time (s)", "BinaryHeap Memory (B)", 
            "DHeap Time (s)", "DHeap Memory (B)", 
            "FibonacciHeap Time (s)", "FibonacciHeap Memory (B)"
        ])
        flattened_results = [
            (item[0], item[1], item[2][0], item[2][1], item[3][0], item[3][1], 
            item[4][0], item[4][1], item[5][0], item[5][1])
            for item in results
        ]
        writer.writerows(flattened_results)
    
    print(f"{Colors.BLUE}Results saved to {filename}.{Colors.RESET}")


def plot_results(results, filename):
    """
    Plot the experiment results by averaging datapoints with the same dataset and heap type.
    
    :param results: A list of tuples (graph_size, radix_time, radix_memory, binary_time, binary_memory, d_heap_time, d_heap_memory, fibonacci_time, fibonacci_memory).
    """

    result_dir = "results"
    filename = os.path.join(result_dir, filename)
    os.makedirs(result_dir, exist_ok=True)

    # Group by graph type and size
    type_grouped = defaultdict(lambda: defaultdict(lambda: {
        "radix_times": [], "radix_memory": [],
        "binary_times": [], "binary_memory": [],
        "d_heap_times": [], "d_heap_memory": [],
        "fibonacci_times": [], "fibonacci_memory": []
    }))

    # Organize results by type and size
    for result in results:
        graph_size, graph_type = result[0], result[1]
        group = type_grouped[graph_type][graph_size]

        group["radix_times"].append(result[2][0])
        group["radix_memory"].append(result[2][1])
        group["binary_times"].append(result[3][0])
        group["binary_memory"].append(result[3][1])
        group["d_heap_times"].append(result[4][0])
        group["d_heap_memory"].append(result[4][1])
        group["fibonacci_times"].append(result[5][0])
        group["fibonacci_memory"].append(result[5][1])

    # Generate plots for each graph type
    for graph_type in type_grouped:
        # Calculate averages
        sizes = sorted(type_grouped[graph_type].keys())
        avg_data = {
            "radix_time": [],
            "radix_memory": [],
            "binary_time": [],
            "binary_memory": [],
            "d_heap_time": [],
            "d_heap_memory": [],
            "fibonacci_time": [],
            "fibonacci_memory": []
        }

        # Calculate averages for each size
        for size in sizes:
            group = type_grouped[graph_type][size]
            avg_data["radix_time"].append(sum(group["radix_times"]) / len(group["radix_times"]))
            avg_data["radix_memory"].append(sum(group["radix_memory"]) / len(group["radix_memory"]))
            avg_data["binary_time"].append(sum(group["binary_times"]) / len(group["binary_times"]))
            avg_data["binary_memory"].append(sum(group["binary_memory"]) / len(group["binary_memory"]))
            avg_data["d_heap_time"].append(sum(group["d_heap_times"]) / len(group["d_heap_times"]))
            avg_data["d_heap_memory"].append(sum(group["d_heap_memory"]) / len(group["d_heap_memory"]))
            avg_data["fibonacci_time"].append(sum(group["fibonacci_times"]) / len(group["fibonacci_times"]))
            avg_data["fibonacci_memory"].append(sum(group["fibonacci_memory"]) / len(group["fibonacci_memory"]))

        # Plot time comparison
        plt.figure(figsize=(14, 6))
        plt.subplot(1, 2, 1)
        plt.plot(sizes, avg_data["radix_time"], 'o-', label="Radix Heap")
        plt.plot(sizes, avg_data["binary_time"], 'o-', label="Binary Heap")
        plt.plot(sizes, avg_data["d_heap_time"], 'o-', label="D-Heap")
        plt.plot(sizes, avg_data["fibonacci_time"], 'o-', label="Fibonacci Heap")

        plt.xlabel("Graph Size (Number of Nodes)")
        plt.ylabel("Average Time Consumed (Seconds)")
        plt.title(f"Time Comparison\nGraph Type: {graph_type}")
        plt.legend()
        plt.grid(True)
        
        # Plot memory comparison as a bar chart
        plt.subplot(1, 2, 2)
        bar_width = 0.2
        x_pos = range(len(sizes))
        
        plt.bar([x - 1.5*bar_width for x in x_pos], avg_data["radix_memory"], width=bar_width, label="Radix Heap")
        plt.bar([x - 0.5*bar_width for x in x_pos], avg_data["binary_memory"], width=bar_width, label="Binary Heap")
        plt.bar([x + 0.5*bar_width for x in x_pos], avg_data["d_heap_memory"], width=bar_width, label="D-Heap")
        plt.bar([x + 1.5*bar_width for x in x_pos], avg_data["fibonacci_memory"], width=bar_width, label="Fibonacci Heap")

        plt.xticks(x_pos, sizes)
        plt.xlabel("Graph Size (Number of Nodes)")
        plt.ylabel("Average Memory Consumed (Bytes)")
        plt.title(f"Memory Comparison\nGraph Type: {graph_type}")
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        # plt.show()

       # Save plot for this graph type
        type_filename = f"{filename}_{graph_type}.jpg"
        plt.savefig(type_filename)
        plt.close()  # Close figure to free memory
        
        print(f"{Colors.BLUE}Plot for '{graph_type}' graphs saved to {type_filename}{Colors.RESET}")

    if len(type_grouped) > 1:
        _plot_combined_results(type_grouped, filename)

def _plot_combined_results(type_grouped, filename):
    """Helper to generate a combined plot showing all graph types."""
    heap_dicts = {
        "Redix": ["radix_times", "radix_memory", "Radix Heap"],
        "Binary": ["binary_times", "binary_memory", "Binary Heap"],
        "DHeap": ["d_heap_times", "d_heap_memory", "D-Heap"],
        "Fibonacci": ["fibonacci_times", "fibonacci_memory", "Fibonacci Heap"]
    }

    for key, value in heap_dicts.items():

        plt.figure(figsize=(14, 8))
        
        # Time comparison
        plt.subplot(2, 1, 1)
        for graph_type in type_grouped:
            sizes = sorted(type_grouped[graph_type].keys())
            avg_times = [
                sum(type_grouped[graph_type][size][value[0]]) / 
                len(type_grouped[graph_type][size][value[0]])
                for size in sizes
            ]
            plt.plot(sizes, avg_times, 'o-', label=f"{graph_type} ({key})")
        
        plt.title(f"Time Comparison Across All Graph Types ({value[2]})")
        plt.xlabel("Graph Size (Nodes)")
        plt.ylabel("Time (seconds)")
        plt.legend()
        plt.grid(True)

        # Memory comparison
        plt.subplot(2, 1, 2)
        for graph_type in type_grouped:
            sizes = sorted(type_grouped[graph_type].keys())
            avg_memory = [
                sum(type_grouped[graph_type][size][value[1]]) / 
                len(type_grouped[graph_type][size][value[1]])
                for size in sizes
            ]
            plt.plot(sizes, avg_memory, 'o-', label=f"{graph_type} ({key})")
        
        plt.title(f"Memory Comparison Across All Graph Types ({value[2]})")
        plt.xlabel("Graph Size (Nodes)")
        plt.ylabel("Memory (bytes)")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        combined_filename = f"{filename}_combined_{key.lower()}.jpg"
        plt.savefig(combined_filename)
        plt.close()
        print(f"{Colors.BLUE}Combined plot saved to {combined_filename}{Colors.RESET}")
from src.helper import Colors
import csv
import matplotlib.pyplot as plt

def save_results_to_csv(results, filename):
    """
    Save the experiment results to a CSV file.
    
    :param results: A list of tuples (graph_size, radix_time, radix_memory, binary_time, binary_memory, d_heap_time, d_heap_memory, fibonacci_time, fibonacci_memory).
    :param filename: The name of the CSV file.
    """
    filename = filename + ".csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Graph Size", 
            "RadixHeap Time (s)", "RadixHeap Memory (B)", 
            "BinaryHeap Time (s)", "BinaryHeap Memory (B)", 
            "DHeap Time (s)", "DHeap Memory (B)", 
            "FibonacciHeap Time (s)", "FibonacciHeap Memory (B)"
        ])
        flattened_results = [
            (item[0], item[1][0], item[1][1], item[2][0], item[2][1], item[3][0], item[3][1], item[4][0], item[4][1])
            for item in results
        ]
        writer.writerows(flattened_results)
    
    print(f"{Colors.BLUE}Results saved to {filename}.{Colors.RESET}")


def plot_results(results, filename):
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

    plt.savefig(f'{filename}.jpg')
    print(f"{Colors.BLUE}Plot image saved to {filename}.jpg.{Colors.RESET}")
import json
import os, re, time
import tracemalloc




from src.dijkstra import dijkstra_shortest_path
from src.load_graph import load_graph_into_radix_heap, load_graph_into_binary_heap, load_graph_into_d_heap, load_graph_into_fibonacci_heap, load_graph

# ANSI color codes
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"  # Reset to default

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
    print(f"\n{Colors.GREEN}Time consumed by Dijkstra's algorithm ({heap_type}): {Colors.RESET}{time_consumed:.6f} seconds")
    
    return shortest_distances

def get_available_datasets():
    """
    Get dataset information without loading entire JSON files.
    Tries to extract info from filenames first, falls back to partial parsing.
    """
    datasets = []
    data_dir = "data"
    if not os.path.exists(data_dir):
        print(f"Directory '{data_dir}' does not exist. Please generate datasets first.")
        return datasets

    for filename in sorted(os.listdir(data_dir)):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(data_dir, filename)
        file_info = {'path': filepath, 'size': None, 'type': 'unknown'}

        # First try to get info from filename pattern (fastest)
        try:
            parts = filename.split('_')
            if len(parts) >= 4:  # Expected format: graph_n{size}_e{edges}_{type}.json
                # Extract size from part like "n5000"
                size_str = parts[1][1:]  # Skip 'n' prefix
                file_info['size'] = int(size_str)
                # Extract type from part like "dense.json"
                file_info['type'] = parts[3].split('.')[0]
                datasets.append((file_info['path'], file_info['size'], file_info['type']))
                continue
        except (IndexError, ValueError):
            pass  # Fall through to JSON parsing

        # If filename parsing failed, try partial JSON reading
        try:
            with open(filepath, 'r') as f:
                nodes_found = False
                node_count = 0
                
                for line in f:
                    if '"nodes":' in line:
                        nodes_found = True
                        # Find the opening bracket
                        while '[' not in line and not line.strip().endswith('['):
                            line = next(f)
                        # Count nodes until closing bracket
                        for line in f:
                            if ']' in line:
                                break
                            node_count += 1
                        break
                
                if nodes_found:
                    file_info['size'] = node_count
                    # Try again to get type from filename
                    parts = filename.split('_')
                    if len(parts) >= 4:
                        file_info['type'] = parts[3].split('.')[0]
                    datasets.append((file_info['path'], file_info['size'], file_info['type']))
                else:
                    print(f"Warning: Couldn't find nodes in {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            continue

    return datasets

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
    d_heap = load_graph_into_d_heap(data_file)  # Use d = max(2, num_edges // num_nodes)
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

def is_valid_input(s):
    # Pattern explanation:
    # ^        - start of string
    # [1-9]    - first digit must be 1-9 (no leading zero)
    # \d*      - zero or more additional digits
    # [dms]?   - optional 'd', 'm', or 's' at the end
    # $        - end of string
    pattern = r'^[1-9]\d*[dms]?$'
    return bool(re.fullmatch(pattern, s))


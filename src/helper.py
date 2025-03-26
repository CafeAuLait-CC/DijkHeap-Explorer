import json
import os, re, time
import tracemalloc
from src.dijkstra import dijkstra_shortest_path
from src.load_graph import load_graph_into_radix_heap, load_graph_into_binary_heap, load_graph_into_d_heap, load_graph_into_fibonacci_heap, load_graph

class Colors:
    """
    ANSI color codes for terminal output formatting.
    """
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
    Execute Dijkstra's algorithm using a specified heap implementation.
    
    Args:
        graph: The graph represented as an adjacency list.
        source_node: Starting node for the algorithm.
        heap: Heap implementation (Radix, Binary, etc.).
        heap_type: String identifier for the heap type (for logging).
        
    Returns:
        Dictionary of shortest distances from source_node.
    """
    print(f"\nRunning Dijkstra's algorithm with {heap_type} from source node {source_node}...")
    
    # Initialize source node distance to 0
    heap.push(0, source_node)
    
    # Time the algorithm execution
    start_time = time.time()
    shortest_distances = dijkstra_shortest_path(graph, source_node, heap)
    end_time = time.time()
    
    time_consumed = end_time - start_time
    print(f"\n{Colors.GREEN}Time consumed by Dijkstra's algorithm ({heap_type}): {Colors.RESET}{time_consumed:.6f} seconds")
    
    return shortest_distances

def get_available_datasets():
    """
    Scan the data directory for available graph datasets.
    
    Returns:
        List of tuples containing (filepath, node_count, graph_type).
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
                size_str = parts[1][1:]  # Skip 'n' prefix
                file_info['size'] = int(size_str)
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
    Run benchmark comparing different heap implementations on a graph.
    
    Args:
        data_file: Path to graph data file.
        graph_size: Number of nodes in the graph.
        
    Returns:
        Tuple of (time, memory) measurements for each heap type.
    """
    # Load and build the graph
    graph, nodes = load_graph(data_file)
    source_node = 0  # Use first node as source
    
    # Benchmark RadixHeap
    tracemalloc.start()
    radix_heap = load_graph_into_radix_heap(data_file)
    start_time = time.time()
    _ = run_dijkstra(graph, source_node, radix_heap, "RadixHeap")
    radix_time = time.time() - start_time
    radix_memory = tracemalloc.get_traced_memory()[1]  # Peak memory usage
    tracemalloc.stop()
    
    # Benchmark BinaryHeap
    tracemalloc.start()
    binary_heap = load_graph_into_binary_heap(data_file)
    start_time = time.time()
    _ = run_dijkstra(graph, source_node, binary_heap, "BinaryHeap")
    binary_time = time.time() - start_time
    binary_memory = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    
    # Benchmark DHeap
    tracemalloc.start()
    d_heap = load_graph_into_d_heap(data_file)
    start_time = time.time()
    _ = run_dijkstra(graph, source_node, d_heap, "DHeap")
    d_heap_time = time.time() - start_time
    d_heap_memory = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    
    # Benchmark FibonacciHeap
    tracemalloc.start()
    fibonacci_heap = load_graph_into_fibonacci_heap(data_file)
    start_time = time.time()
    _ = run_dijkstra(graph, source_node, fibonacci_heap, "FibonacciHeap")
    fibonacci_time = time.time() - start_time
    fibonacci_memory = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    
    return (
        (radix_time, radix_memory),
        (binary_time, binary_memory),
        (d_heap_time, d_heap_memory),
        (fibonacci_time, fibonacci_memory)
    )

def is_valid_input(s):
    """
    Validate user input for graph generation parameters.
    
    Args:
        s: Input string to validate.
        
    Returns:
        True if input matches expected pattern, False otherwise.
    """
    pattern = r'^[1-9]\d*[dms]?$'
    return bool(re.fullmatch(pattern, s))
import json
import time
from radix_heap import RadixHeap
from binary_heap import BinaryHeap
from dijkstra import dijkstra_shortest_path, build_graph_from_edges

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
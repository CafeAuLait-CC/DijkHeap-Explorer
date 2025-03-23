from helper import load_graph_into_radix_heap, load_graph_into_binary_heap
from helper import load_graph, run_dijkstra, print_shortest_distances


def main():
    # Step 1: Load and build the graph
    data_file = "data/large_graph.json"  # Path to the graph file
    graph, nodes = load_graph(data_file)
    
    # Step 2: Define the source node
    source_node = 0  # Source node for Dijkstra's algorithm
    
    # Step 3: Run Dijkstra's algorithm with both RadixHeap and BinaryHeap
    heap_types = [
        ("RadixHeap", load_graph_into_radix_heap(data_file)),
        ("BinaryHeap", load_graph_into_binary_heap(data_file))
    ]
    
    for heap_type, heap in heap_types:
        shortest_distances = run_dijkstra(graph, source_node, heap, heap_type)
        print_shortest_distances(shortest_distances, heap_type)

if __name__ == "__main__":
    main()
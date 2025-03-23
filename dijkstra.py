from radix_heap import RadixHeap
from binary_heap import BinaryHeap

def dijkstra_shortest_path(graph, source, heap):
    """
    Dijkstra's shortest path algorithm using a generic heap.
    
    :param graph: A dictionary representing the graph. Keys are nodes, and values are lists of tuples (neighbor, weight).
    :param source: The source node.
    :param heap: A heap object (RadixHeap or BinaryHeap) that supports push(), pop(), and is_empty().
    :return: A dictionary containing the shortest distance from the source to each node.
    """
    # Initialize distances
    distances = {node: float('inf') for node in graph}
    distances[source] = 0  # Distance from source to itself is 0
    
    # Initialize the heap
    heap.push(0, source)  # Push the source node with distance 0
    
    # Process nodes in the heap
    while not heap.is_empty():
        current_node, current_distance = heap.pop()
        
        # If the current distance is greater than the recorded distance, skip
        if current_distance > distances[current_node]:
            continue
        
        # Explore neighbors
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            # If a shorter path is found, update the distance and push to the heap
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heap.push(distance, neighbor)
    
    return distances

def build_graph_from_edges(nodes, edges):
    """
    Build a graph representation from a list of nodes and edges.
    
    :param nodes: List of nodes.
    :param edges: List of edges, where each edge is a tuple (u, v, weight).
    :return: A dictionary representing the graph.
    """
    graph = {node: [] for node in nodes}
    for u, v, weight in edges:
        graph[u].append((v, weight))  # Add edge from u to v
        graph[v].append((u, weight))  # Add edge from v to u (undirected)
    return graph

def main():
    # Example graph
    nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    edges = [
        (0, 9, 9), (0, 4, 3), (1, 2, 1), (1, 7, 8), (1, 3, 7), (1, 6, 9), (1, 8, 2),
        (3, 6, 2), (3, 5, 7), (4, 9, 8), (4, 6, 10), (4, 7, 6), (6, 9, 1), (6, 7, 1)
    ]
    
    # Build the graph
    graph = build_graph_from_edges(nodes, edges)
    
    # Run Dijkstra's algorithm with RadixHeap
    print("Running Dijkstra's algorithm with RadixHeap...")
    radix_heap = RadixHeap()
    shortest_distances_radix = dijkstra_shortest_path(graph, source=0, heap=radix_heap)
    print("Shortest distances (RadixHeap):", shortest_distances_radix)
    
    # Run Dijkstra's algorithm with BinaryHeap
    print("\nRunning Dijkstra's algorithm with BinaryHeap...")
    binary_heap = BinaryHeap()
    shortest_distances_binary = dijkstra_shortest_path(graph, source=0, heap=binary_heap)
    print("Shortest distances (BinaryHeap):", shortest_distances_binary)

if __name__ == "__main__":
    main()
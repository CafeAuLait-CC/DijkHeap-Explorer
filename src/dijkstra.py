def build_graph_from_edges(nodes, edges):
    """Build adjacency list representation from edges.
    
    Args:
        nodes: List of nodes in the graph.
        edges: List of edges (u, v, weight) for weighted or (u, v) for unweighted.
        
    Returns:
        Adjacency list representation of the graph.
    """
    graph = {node: [] for node in nodes}  # Initialize with empty lists
    for edge in edges:
        if len(edge) == 3:  # Undirected graph (u, v, weight)
            u, v, weight = edge
            graph[u].append((v, weight))
            graph[v].append((u, weight))  # Add both directions for undirected
        elif len(edge) == 2:  # Directed graph (u, v) with implicit weight=1
            u, v = edge
            graph[u].append((v, 1))
    return graph

def dijkstra_shortest_path(graph, source, heap):
    """Dijkstra's shortest path algorithm using a generic heap.
    
    Args:
        graph: Adjacency list where keys are nodes and values are lists of 
              (neighbor, weight) tuples.
        source: The source node.
        heap: A heap object supporting push(), pop(), and is_empty().
        
    Returns:
        Dictionary containing shortest distance from source to each node.
    """
    INF = float('inf')
    distances = {node: INF for node in graph}
    distances[source] = 0

    # Initialize heap
    if hasattr(heap, 'contains') and heap.contains(source):
        heap.decrease_key(source, 0)
    else:
        heap.push(0, source)

    while not heap.is_empty():
        current_node, current_distance = heap.pop()
        
        # Skip if we've already found a better path
        if current_distance > distances[current_node]:
            continue
        
        # Explore neighbors
        for neighbor, weight in graph.get(current_node, []):
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                if hasattr(heap, 'contains') and heap.contains(neighbor):
                    heap.decrease_key(neighbor, distance)
                else:
                    heap.push(distance, neighbor)
    
    return distances

def main():
    """Example usage of Dijkstra's algorithm with different heaps."""
    from src.radix_heap import RadixHeap
    from src.binary_heap import BinaryHeap

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
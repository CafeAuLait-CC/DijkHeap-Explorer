import json
import random

def generate_weighted_graph(num_nodes, num_edges, weight_range=(1, 10)):
    """Generate a weighted undirected graph with specified parameters.
    
    Args:
        num_nodes: Number of nodes in the graph.
        num_edges: Number of edges in the graph.
        weight_range: Tuple (min_weight, max_weight) for edge weights.
        
    Returns:
        A dictionary representing the graph with "nodes" and "edges" keys.
    """
    nodes = list(range(num_nodes))
    edges = set()
    
    # Generate unique edges until we reach the desired count
    while len(edges) < num_edges:
        u = random.choice(nodes)
        v = random.choice(nodes)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            weight = random.randint(weight_range[0], weight_range[1])
            edges.add((u, v, weight))
    
    return {
        "nodes": nodes,
        "edges": list(edges)
    }

def save_graph_to_disk(graph, filename):
    """Save a graph to a JSON file.
    
    Args:
        graph: The graph dictionary to save.
        filename: The name/path of the file to save to.
    """
    with open(filename, 'w') as f:
        json.dump(graph, f)
    
    print(f"Graph saved to {filename}")

if __name__ == "__main__":
    # Generate a larger graph (10x more nodes and edges)
    num_nodes = 100  # 10x more nodes
    num_edges = 500  # 10x more edges
    graph = generate_weighted_graph(num_nodes, num_edges)
    
    # Save the graph to disk
    save_graph_to_disk(graph, "large_graph.json")
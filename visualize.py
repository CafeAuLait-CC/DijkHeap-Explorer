import json
import matplotlib.pyplot as plt
import networkx as nx

def load_graph_from_json(filepath):
    """
    Load an UNDIRECTED graph from a JSON file.
    """
    with open(filepath, 'r') as f:
        graph_data = json.load(f)
    
    # Create an undirected graph
    G = nx.Graph()
    
    # Add nodes
    G.add_nodes_from(graph_data["nodes"])
    
    # Add edges with weights
    for u, v, weight in graph_data["edges"]:
        G.add_edge(u, v, weight=weight)
    
    return G

def visualize_graph(graph, layout="spring", k=None):
    """
    Visualize the UNDIRECTED graph using matplotlib.
    
    :param graph: A NetworkX graph object.
    :param layout: Layout algorithm to use ("spring", "circular", "shell", "kamada_kawai", "spectral", "random").
    :param k: Optimal distance between nodes (for spring layout).
    """
    # Choose layout algorithm
    if layout == "spring":
        pos = nx.spring_layout(graph, k=k)  # Adjust k for better spacing
    elif layout == "circular":
        pos = nx.circular_layout(graph)
    elif layout == "shell":
        pos = nx.shell_layout(graph)
    elif layout == "kamada_kawai":
        pos = nx.kamada_kawai_layout(graph)
    elif layout == "spectral":
        pos = nx.spectral_layout(graph)
    elif layout == "random":
        pos = nx.random_layout(graph)
    else:
        raise ValueError(f"Unknown layout: {layout}")
    
    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_size=500, node_color='lightblue')
    
    # Draw edges
    nx.draw_networkx_edges(graph, pos, edge_color='gray')
    
    # Draw edge labels (weights)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    
    # Draw node labels
    nx.draw_networkx_labels(graph, pos, font_size=12, font_color='black')
    
    # Display the graph
    plt.title(f"Undirected Graph Visualization ({layout} layout)")
    plt.axis('off')  # Turn off the axis
    plt.show()

def main():
    # Load the graph from the JSON file
    data_file = "data/graph_example.json"
    print(f"Loading graph from {data_file}...")
    graph = load_graph_from_json(data_file)
    
    # Visualize the graph with different layouts
    print("Visualizing the graph...")
    
    # Try different layouts
    # visualize_graph(graph, layout="spring", k=0.5)  # Adjust k for better spacing
    # visualize_graph(graph, layout="circular")
    visualize_graph(graph, layout="shell")
    # visualize_graph(graph, layout="kamada_kawai")
    # visualize_graph(graph, layout="spectral")

if __name__ == "__main__":
    main()
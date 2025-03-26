import os
from src.helper import Colors, run_experiment, get_available_datasets, is_valid_input
from src.generate_data import generate_weighted_graph, save_graph_to_disk
from src.stats import save_results_to_csv, plot_results
from datetime import datetime

def generate_graphs():
    """
    Generate new graph datasets based on user input for benchmarking.
    
    Handles user input for graph sizes and types (dense/sparse/middle),
    then generates and saves the corresponding graphs to the data directory.
    """
    print("\n--- Generate New Datasets ---")
    print("Enter a list of graph sizes (e.g., 1000, 2000 or [1000, 2000]):")
    print("- Tips: add 'd', 's', 'm' in the end to specify graph types 'dense', 'sparse' and 'middle(average)', e.g. 100s, 200s, 300s")
    user_input = input("Graph sizes: ").strip()
    
    # Parse the user input
    if user_input.startswith("[") and user_input.endswith("]"):
        user_input = user_input[1:-1]  # Remove brackets

    # Verify user input and extract graph specifications
    graph_sizes = []
    invalid_input = []
    input_list = [size.strip() for size in user_input.split(",")]

    for item in input_list:
        if is_valid_input(item):
            if item.isdecimal():
                graph_sizes.append((int(item), "random"))
            else:
                graph_type_flag = item[-1]
                graph_type = "dense" if graph_type_flag == 'd' else "sparse" if graph_type_flag == 's' else "middle"
                graph_sizes.append((int(item[:-1]), graph_type))
        else:
            invalid_input.append(item)
    if len(invalid_input) > 0:
        print("Found invalid input, skipping:", invalid_input)

    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
        
    # Generate graphs based on specifications
    for item in graph_sizes:
        size = item[0]
        type = item[1]
        print(f"\nGenerating graph with {size} nodes...")
        # Calculate edges based on graph type
        sparse_edge = size * 2
        dense_edge = size * (size - 1) // 2
        num_edges = sparse_edge if type == "sparse" else dense_edge if type == "dense" else (sparse_edge + dense_edge) // 2 if type == "middle" else size * 5
        graph = generate_weighted_graph(num_nodes=size, num_edges=num_edges)
        filename = f"graph_n{size}_e{num_edges}_{type}.json"
        filepath = os.path.join(data_dir, filename)
        save_graph_to_disk(graph, filepath)
    
    print("\nDataset generation completed.")

def main_menu():
    """
    Main menu interface for the Dijkstra's algorithm benchmark tool.
    
    Provides options to:
    - List available datasets
    - Generate new datasets
    - Run benchmarks
    - View previous results
    - Exit the program
    """
    results = []  # Stores benchmark results for the current session
    
    while True:
        print(f"\n{Colors.CYAN}--- Dijkstra's Algorithm Performance Comparison ---{Colors.RESET}")
        print(f"{Colors.YELLOW}1. [L]ist all datasets (graphs){Colors.RESET}")
        print(f"{Colors.YELLOW}2. [G]enerate new datasets (graphs){Colors.RESET}")
        print(f"{Colors.YELLOW}3. [R]un benchmark on all available datasets{Colors.RESET}")
        print(f"{Colors.YELLOW}4. [V]iew previous results{Colors.RESET}")
        print(f"0. [E]xit")
        
        choice = input("\nEnter your choice: ").strip().lower()

        # Handle menu choices
        if choice in ["1", "l"]:
            datasets = get_available_datasets()
            for data in datasets:
                print(f"Graph file: {data[0]}, Size: {data[1]}")
        
        elif choice in ["2", "g"]:
            generate_graphs()
        
        elif choice in ["3", "r"]:
            print("\n - Running Dijkstra's algorithm on all available datasets...")
            datasets = get_available_datasets()
            if not datasets:
                print("No datasets found in the /data folder. Please generate datasets first.")
            else:
                for filepath, graph_size, graph_type in datasets:
                    print(f"\n{Colors.MAGENTA}Running benchmark on {filepath} (Size: {graph_size}, Type: {graph_type})...{Colors.RESET}")
                    radix, binary, d_heap, fibonacci = run_experiment(filepath, graph_size)
                    results.append((graph_size, graph_type, radix, binary, d_heap, fibonacci))
                    print(f"{Colors.GREEN}Done.{Colors.RESET}")

            # Save results with timestamp
            current_timestamp = datetime.now().strftime("%y%m%d%H%M%S")
            filename_plot = "plot-" + current_timestamp
            filename_csv = "results-" + current_timestamp

            if results:
                plot_results(results, filename_plot)
                save_results_to_csv(results, filename_csv)
            else:
                print("\nNo results to save/plot. Please run a benchmark first.")
        
        elif choice in ["4", "v"]:
            if not results:
                print("\nNo results to display. Please run a benchmark first.")
            else:
                print("\nResults:")
                for result in results:
                    print(f"{Colors.MAGENTA}Graph Size: {result[0]}{Colors.RESET}")
                    print(f"Graph Type: {result[1]}")
                    print(f"RadixHeap: Time={result[2][0]:.6f}s, Memory={result[2][1]}B")
                    print(f"BinaryHeap: Time={result[3][0]:.6f}s, Memory={result[3][1]}B")
                    print(f"DHeap: Time={result[4][0]:.6f}s, Memory={result[4][1]}B")
                    print(f"FibonacciHeap: Time={result[5][0]:.6f}s, Memory={result[5][1]}B")
                    print()            
        
        elif choice in ["0", "e"]:
            print("\nExiting the program. Goodbye!")
            exit(0)
        
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
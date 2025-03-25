import os

from src.helper import Colors, run_experiment, get_available_datasets, is_valid_input
from src.generate_data import generate_weighted_graph, save_graph_to_disk
from src.stats import save_results_to_csv, plot_results

from datetime import datetime





def generate_graphs():
    """
    Generate new datasets (graphs) based on user input.
    """
    print("\n--- Generate New Datasets ---")
    print("Enter a list of graph sizes (e.g., 1000, 2000 or [1000, 2000]):")
    user_input = input("Graph sizes: ").strip()
    
    # Parse the user input
    if user_input.startswith("[") and user_input.endswith("]"):
        user_input = user_input[1:-1]  # Remove brackets

    # Verify user input
    graph_sizes = {}
    invalid_input = []
    input_list = [size.strip() for size in user_input.split(",")]

    for item in input_list:
        if is_valid_input(item):
            if item.isdecimal():
                graph_sizes[int(item)] = "random"
            else:
                graph_types = item[-1]
                graph_sizes[int(item[:-1])] = "dense" if graph_type == 'd' else "sparse" if graph_type == 's' else "middle"
        else:
            invalid_input.append(item)
    if len(invalid_input) > 0:
        print("Found invalid input, skipping:", invalid_input)


    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
        
    # Generate graphs
    for size, type in graph_sizes.items():
        print(f"\nGenerating graph with {size} nodes...")
        sparse_edge = size * 2
        dense_edge = size * (size - 1) / 2
        num_edges = sparse_edge if type == "sparse" else dense_edge if type == "dense" else (sparse_edge + dense_edge) / 2 if type == "middle" else size * 5
        graph = generate_weighted_graph(num_nodes=size, num_edges=num_edges)  # Adjust num_edges as needed
        filename = f"graph_n{size}_e{num_edges}_{type}.json"
        filepath = os.path.join(data_dir, filename)
        save_graph_to_disk(graph, filepath)
    
    print("\nDataset generation completed.")


def main_menu():
    """
    Display the main menu and handle user input.
    """
    results = []
    
    while True:
        print(f"\n{Colors.CYAN}--- Dijkstra's Algorithm Performance Comparison ---{Colors.RESET}n")
        print(f"{Colors.YELLOW}1. List all datasets (graphs){Colors.RESET}")
        print(f"{Colors.YELLOW}2. Generate new datasets (graphs){Colors.RESET}")
        print(f"{Colors.YELLOW}3. Run experiment on all available datasets{Colors.RESET}")
        print(f"{Colors.YELLOW}4. View previous results{Colors.RESET}")
        print(f"0. Exit")
        
        choice = input("\nEnter your choice: ")

        match choice:

            case "1":
                datasets = get_available_datasets()
                for data in datasets:
                    print(f"Graph file: {data[0]}, Size: {data[1]}")
        
            case "2":
                generate_graphs()
        
            case "3":
                print("\n - Running Dijkstra's algorithm on all available datasets...")
                datasets = get_available_datasets()
                if not datasets:
                    print("No datasets found in the /data folder. Please generate datasets first.")
                else:
                    for filepath, graph_size in datasets:
                        print(f"\n{Colors.MAGENTA}Running experiment on {filepath} (Size: {graph_size})...{Colors.RESET}")
                        radix, binary, d_heap, fibonacci = run_experiment(filepath, graph_size)
                        results.append((graph_size, radix, binary, d_heap, fibonacci))
                        print(f"{Colors.GREEN}Done.{Colors.RESET}")

                current_timestamp = datetime.now().strftime("%y%m%d%H%M%S")
                filename = "results-" + current_timestamp

                # Plot results
                if not results:
                    print("\nNo results to plot. Please run an experiment first.")
                else:
                    plot_results(results, filename)

                # Save results into csv
                if not results:
                    print("\nNo results to save. Please run an experiment first.")
                else:
                    save_results_to_csv(results, filename)
        
            case "4":
                if not results:
                    print("\nNo results to display. Please run an experiment first.")
                else:
                    print("\nResults:")
                    for result in results:
                        print(f"Graph Size: {result[0]}")
                        print(f"RadixHeap: Time={result[1][0]:.6f}s, Memory={result[1][1]}B")
                        print(f"BinaryHeap: Time={result[2][0]:.6f}s, Memory={result[2][1]}B")
                        print(f"DHeap: Time={result[3][0]:.6f}s, Memory={result[3][1]}B")
                        print(f"FibonacciHeap: Time={result[4][0]:.6f}s, Memory={result[4][1]}B")
                        print()            
        
            case "0":
                print("\nExiting the program. Goodbye!")
                exit(0)
        
            case _:
                print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
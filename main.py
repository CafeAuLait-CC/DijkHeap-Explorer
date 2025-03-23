import os

from helper import run_experiment, save_results_to_csv, plot_results
from generate_data import generate_weighted_graph, save_graph_to_disk

def generate_graphs():
    """
    Generate new datasets (graphs) based on user input.
    """
    print("\n--- Generate New Datasets ---")
    print("Enter a list of graph sizes (e.g., 2000, 3000 or [2000, 3000]):")
    user_input = input("Graph sizes: ").strip()
    
    # Parse the user input
    if user_input.startswith("[") and user_input.endswith("]"):
        user_input = user_input[1:-1]  # Remove brackets
    graph_sizes = [int(size.strip()) for size in user_input.split(",")]

    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    filepath = os.path.join(data_dir, filename)
    
    # Generate graphs
    for size in graph_sizes:
        print(f"\nGenerating graph with {size} nodes...")
        graph = generate_weighted_graph(num_nodes=size, num_edges=size * 5)  # Adjust num_edges as needed
        filename = f"graph_{size}_nodes.json"
        filepath = os.path.join(data_dir, filename)
        save_graph_to_disk(graph, filepath)
    
    print("\nDataset generation completed.")

def main_menu():
    """
    Display the main menu and handle user input.
    """
    results = []
    
    while True:
        print("\n--- Dijkstra's Algorithm Performance Comparison ---")
        print("1. Run experiment on small graph (10 nodes)")
        print("2. Run experiment on large graph (100 nodes)")
        print("3. Generate new datasets (graphs)")
        print("4. Run custom experiment")
        print("5. View results")
        print("6. Save results to CSV")
        print("7. Plot results")
        print("8. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            print("\nRunning experiment on small graph...")
            radix, binary, d_heap, fibonacci = run_experiment("data/graph_example.json", 10)
            results.append((10, radix, binary, d_heap, fibonacci))
            print("Experiment completed.")
        
        elif choice == "2":
            print("\nRunning experiment on large graph...")
            radix, binary, d_heap, fibonacci = run_experiment("data/large_graph.json", 100)
            results.append((100, radix, binary, d_heap, fibonacci))
            print("Experiment completed.")
        
        elif choice == "3":
            generate_graphs()
        
        elif choice == "4":
            data_file = input("Enter the path to the graph file: ")
            graph_size = int(input("Enter the number of nodes in the graph: "))
            print(f"\nRunning experiment on custom graph ({graph_size} nodes)...")
            radix, binary, d_heap, fibonacci = run_experiment(data_file, graph_size)
            results.append((graph_size, radix, binary, d_heap, fibonacci))
            print("Experiment completed.")
        
        elif choice == "5":
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
        
        elif choice == "6":
            if not results:
                print("\nNo results to save. Please run an experiment first.")
            else:
                filename = input("Enter the filename to save results (e.g., results.csv): ")
                save_results_to_csv(results, filename)
        
        elif choice == "7":
            if not results:
                print("\nNo results to plot. Please run an experiment first.")
            else:
                plot_results(results)
        
        elif choice == "8":
            print("\nExiting the program. Goodbye!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
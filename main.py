from helper import plot_results, run_experiment, save_results_to_csv

def main_menu():
    """
    Display the main menu and handle user input.
    """
    results = []
    
    while True:
        print("\n--- Dijkstra's Algorithm Performance Comparison ---")
        print("1. Run experiment on small graph (10 nodes)")
        print("2. Run experiment on large graph (100 nodes)")
        print("3. Run custom experiment")
        print("4. View results")
        print("5. Save results to CSV")
        print("6. Plot results")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            print("\nRunning experiment on small graph...")
            radix_time, binary_time, d_heap_time, fibonacci_time = run_experiment("data/graph_example.json", 10)
            results.append((10, radix_time, binary_time, d_heap_time, fibonacci_time))
            print("Experiment completed.")
        
        elif choice == "2":
            print("\nRunning experiment on large graph...")
            radix_time, binary_time, d_heap_time, fibonacci_time = run_experiment("data/large_graph.json", 100)
            results.append((100, radix_time, binary_time, d_heap_time, fibonacci_time))
            print("Experiment completed.")
        
        elif choice == "3":
            data_file = input("Enter the path to the graph file: ")
            graph_size = int(input("Enter the number of nodes in the graph: "))
            print(f"\nRunning experiment on custom graph ({graph_size} nodes)...")
            radix_time, binary_time, d_heap_time, fibonacci_time = run_experiment(data_file, graph_size)
            results.append((graph_size, radix_time, binary_time, d_heap_time, fibonacci_time))
            print("Experiment completed.")
        
        elif choice == "4":
            if not results:
                print("\nNo results to display. Please run an experiment first.")
            else:
                print("\nResults:")
                for result in results:
                    print(f"Graph Size: {result[0]}, RadixHeap: {result[1]:.6f}s, BinaryHeap: {result[2]:.6f}s, DHeap: {result[3]:.6f}s, FibonacciHeap: {result[4]:.6f}s")
        
        elif choice == "5":
            if not results:
                print("\nNo results to save. Please run an experiment first.")
            else:
                filename = input("Enter the filename to save results (e.g., results.csv): ")
                save_results_to_csv(results, filename)
        
        elif choice == "6":
            if not results:
                print("\nNo results to plot. Please run an experiment first.")
            else:
                plot_results(results)
        
        elif choice == "7":
            print("\nExiting the program. Goodbye!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
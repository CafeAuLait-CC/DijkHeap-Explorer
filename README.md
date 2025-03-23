# DijkHeap Explorer

DijkHeap Explorer is a Python-based tool designed to compare the performance of Dijkstra's shortest path algorithm using different heap implementations (BinaryHeap, DHeap, FibonacciHeap and RadixHeap) on various graph datasets.

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/DijkHeapExplorer.git
   cd DijkHeapExplorer
   ```

2. **Create a Virtual Environment:**
   - Using `conda`:
     ```bash
     conda create -n dijkheap_env
     conda activate dijkheap_env
     ```
   - Using `venv`:
     ```bash
     python -m venv dijkheap_env
     source dijkheap_env/bin/activate  # On Windows use `dijkheap_env\Scripts\activate`
     ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start the program, run:
```bash
python run.py
```

### Main Menu Options

You will see the main menu of this program:
```
--- Dijkstra's Algorithm Performance Comparison ---
1. Run experiment on small graph (10 nodes)
2. Run experiment on all available datasets
3. Generate new datasets (graphs)
4. Run custom experiment
5. View results
6. Save results to CSV
7. Plot results
8. Exit
Enter your choice: 
```

1. **Run experiment on small graph (10 nodes):**
   - **Command:** Select option `1` from the main menu.
   - **Expected Output:**
     ```
     Running experiment on small graph...
     Experiment completed.
     ```

2. **Run experiment on all available datasets:**
   - **Command:** Select option `2` from the main menu.
   - **Expected Output:**
     ```
     Running experiment on all available datasets...
     Running experiment on data/graph_2000_nodes.json (Size: 2000)...
     Experiment completed.
     Running experiment on data/graph_3000_nodes.json (Size: 3000)...
     Experiment completed.
     ```

3. **Generate new datasets (graphs):**
   - **Command:** Select option `3` from the main menu.
   - **Expected Output:**
     ```
     --- Generate New Datasets ---
     Enter a list of graph sizes (e.g., 2000, 3000 or [2000, 3000]):
     Graph sizes: 2000, 3000
     Generating graph with 2000 nodes...
     Generating graph with 3000 nodes...
     Dataset generation completed.
     ```

4. **Run custom experiment:**
   - **Command:** Select option `4` from the main menu.
   - **Expected Output:**
     ```
     Enter the path to the graph file: data/graph_2000_nodes.json
     Enter the number of nodes in the graph: 2000
     Running experiment on custom graph (2000 nodes)...
     Experiment completed.
     ```

5. **View results:**
   - **Command:** Select option `5` from the main menu.
   - **Expected Output:**
     ```
     Results:
     Graph Size: 2000
     RadixHeap: Time=0.123456s, Memory=1024B
     BinaryHeap: Time=0.234567s, Memory=2048B
     DHeap: Time=0.345678s, Memory=3072B
     FibonacciHeap: Time=0.456789s, Memory=4096B
     ```

6. **Save results to CSV:**
   - **Command:** Select option `6` from the main menu.
   - **Expected Output:**
     ```
     Enter the filename to save results (e.g., results.csv): results.csv
     Results saved to results.csv.
     ```

7. **Plot results:**
   - **Command:** Select option `7` from the main menu.
   - **Expected Output:**
     ```
     Plotting results...
     ```

8. **Exit:**
   - **Command:** Select option `8` from the main menu.
   - **Expected Output:**
     ```
     Exiting the program. Goodbye!
     ```

## File Structure

The file structure of this project list as follows:
```

DijkHeapExplorer/
├── data/
│   └── graph_100_nodes.json
├── src/
│   ├── __init__.py
│   ├── generate_data.py
│   ├── helper.py
│   ├── binary_heap.py
│   ├── d_heap.py
│   ├── fibonacci_heap.py
│   ├── radix_heap.py
│   └── dijkstra.py
├── tests/
│   ├── __init__.py
│   └── test_*.py
├── run.py
├── README.md
└── requirements.txt
```


## Acknowledgement

This project is build with the help of generative AI [DeepSeek V3](www.deepseek.com).

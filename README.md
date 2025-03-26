# DijkHeap Explorer

DijkHeap Explorer is a Python-based tool designed to compare the performance of Dijkstra's shortest path algorithm using different heap implementations (BinaryHeap, DHeap, FibonacciHeap and RadixHeap) on various graph datasets.

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/CafeAuLait-CC/DijkHeap-Explorer.git
   cd DijkHeap-Explorer
   ```

2. **Create a Virtual Environment:**
   
   Using `conda`:
   ```bash
   conda create -n dijkheap_env python=3.8
   conda activate dijkheap_env
   ```
   Using `venv`:
   ```bash
   python -m venv dijkheap_env
   source dijkheap_env/bin/activate  # On Windows use `dijkheap_env\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start the interactive UI, run:
```bash
python run.py
```

### Interactive UI Features

```
--- Dijkstra's Algorithm Performance Comparison ---

1. [L]ist all datasets (graphs)
2. [G]enerate new datasets (graphs)
3. [R]un benchmark on all available datasets
4. [V]iew previous results
0. [E]xit

Enter your choice: 
```

### Detailed Usage Guide

1. **List Available Datasets**
   - **Command:** Press `1` or `L`
   - **Description:** Shows all available graph datasets in the `/data` directory
   - **Example Output:**
     ```
     Graph file: data/graph_n100_e500_middle.json, Size: 100, Type: middle
     Graph file: data/graph_n1000_e5000_sparse.json, Size: 1000, Type: sparse
     ```

2. **Generate New Datasets**
   - **Command:** Press `2` or `G`
   - **Description:** Create new graph datasets with custom sizes and densities
   - **Input Format:** 
     - Enter sizes like `100, 200, 300` for random density
     - Add `d`/`s`/`m` suffix for dense/sparse/middle (e.g., `100s, 200d, 300m`)
   - **Example Session:**
     ```
     Enter a list of graph sizes (e.g., 1000, 2000 or [1000, 2000]):
     Tips: add 'd', 's', 'm' for dense/sparse/middle types (e.g. 100s, 200d)
     Graph sizes: 100, 200s, 300d, 400m
     
     Generating graph with 100 nodes (random density)...
     Generating graph with 200 nodes (sparse)...
     Generating graph with 300 nodes (dense)...
     Generating graph with 400 nodes (middle density)...
     Dataset generation completed.
     ```

3. **Run Benchmark Tests**
   - **Command:** Press `3` or `R`
   - **Description:** Runs Dijkstra's algorithm on all available datasets using all heap types
   - **Example Output:**
     ```
     Running benchmark on data/graph_n100_e500_random.json (Size: 100, Type: random)...

     Running Dijkstra's algorithm with RadixHeap from source node 0...

     Time consumed by Dijkstra's algorithm (RadixHeap): 0.001941 seconds

     Running Dijkstra's algorithm with BinaryHeap from source node 0...

     Time consumed by Dijkstra's algorithm (BinaryHeap): 0.000760 seconds

     Running Dijkstra's algorithm with DHeap from source node 0...

     Time consumed by Dijkstra's algorithm (DHeap): 0.000507 seconds

     Running Dijkstra's algorithm with FibonacciHeap from source node 0...

     Time consumed by Dijkstra's algorithm (FibonacciHeap): 0.001710 seconds
     Done.
     Plot for 'random' graphs saved to results/plot-250325232538_random.jpg
     Results saved to results/results-250325232538.csv.
     ```

4. **View Results**
   - **Command:** Press `4` or `V`
   - **Description:** Shows detailed benchmark results from current session
   - **Example Output:**
     ```
     Results:
     Graph Size: 100
     Graph Type: random
     RadixHeap: Time=0.002047s, Memory=69460B
     BinaryHeap: Time=0.000816s, Memory=111572B
     DHeap: Time=0.000526s, Memory=66756B
     FibonacciHeap: Time=0.001736s, Memory=66756B
     ```

5. **Automatic Result Saving**
   - Benchmark results are automatically saved with timestamp to:
     - CSV file in `/results` directory
     - Plots comparing performance metrics

6. **Exit Program**
   - **Command:** Press `0` or `E`
   - **Description:** End the program
   - **Example Output:**
     ```
     Exiting the program. Goodbye!
     ```

### Advanced Features

- **Graph Types:**
  - Sparse graphs (~2 edges per node)
  - Dense graphs (~n² edges)
  - Middle density (balanced edges)

- **Heap Implementations:**
  - RadixHeap: Optimized for integer weights
  - BinaryHeap: Standard binary heap
  - DHeap: Configurable branching factor
  - FibonacciHeap: Amortized O(1) operations

## File Structure

```
DijkHeap-Explorer/
│
├── cpp_ver/                # C++ implementation of the core features, 
│   ├── include/            # just as reference and assist with python code analyzation
│   │   └── *.hpp           # C++ headers
│   ├── src/
│   │   └── *.cpp           # C++ source code
│   │ 
│   └── Makefile            # C++ project Makefile
│
├── data/                   # Graph datasets
│   └── graph_n100_e500_random.json
│
├── results/                # Benchmark results
│   ├── *.jpg               # Performance plots
│   └── *.csv               # Result CSVs
│
├── src/
│   ├── __init__.py
│   ├── binary_heap.py      # Binary heap implementation
│   ├── d_heap.py           # D-ary heap implementation
│   ├── dijkstra.py         # Dijkstra's algorithm
│   ├── fibonacci_heap.py   # Fibonacci heap
│   ├── generate_data.py    # Graph generator
│   ├── helper.py           # Utilities
│   ├── load_graph.py       # Graph loader
│   └── radix_heap.py       # Radix heap
│
├── tests/                  # Unit tests
│   ├── __init__.py
│   └── test_*.py           
│
├── run.py                  # Main entry point **
├── README.md
└── requirements.txt
```

## Unit Test

Run unit tests:
```bash
python -m unittest
```

## Acknowledgement

This project was developed with assistance of Generative AI **[You Know Who]**.
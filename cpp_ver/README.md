# C++ Implementation

Due to the way Python programming language is designed, it is not good at high performance computation compared to C, C++ or other high performance programming languages, some heap structure cannot be implemented to achieve the theoretical performance using Python.

Thus, we provide a C++ implementation of the core feature of this project: Binary Heap, D-Heap, Fabonacci Heap, Radix Heap and Dijkstra's Shortest Path algorithm.

To run the C++ program, you will first need to compile the source code using any tools you prefer. 

In this project, we provide a Makefile so that you can easily compile and run it using `make` and `g++` with the following command:

```
cd cpp_ver
make
./dijkstra ../data/graph_n100_e500_random.json
```

And of course you can use any other tools that you are familiar with. (E.g. IDEs, like Visual Studio, CLion, Xcode) 

You need to provide the path to a json file that is storing a graph. The program will run the Dijkstra's algorithm on all four heaps with the provided json graph.

Only one json file is accepted for each run. To test on a different json graph, you will need to run the program again.

This program is only for reference and help analyze the Python main program's performance.
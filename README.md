# Genetic Algorithm for Traveling Salesman Problem (TSP)

This project implements a **Genetic Algorithm (GA)** to solve the **Traveling Salesman Problem (TSP)** in Python. It supports various **selection, crossover, and mutation strategies** and provides visualizations for routes, fitness, and distance progression over generations.

## Features

- Supports **different selection strategies**: tournament, roulette, rank
- Supports **crossover strategies**: order crossover, one-point, two-point, uniform
- Supports **mutation strategies**: swap, inversion, scramble
- Tracks and plots **fitness history** and **distance history**
- Visualizes the **best route found** on a 2D map of cities
- Reads TSP datasets (e.g., `.tsp` files)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/genetic-tsp-solver.git
cd genetic-tsp-solver
```

2. Install dependencies:
```bash
pip install matplotlib
```
## Usage
1. Place your TSP dataset in the data/ folder (i have placed a test dataset in data folder).
2. Run the main script:

```bash
python main.py
```

The script will output:

- Best route found
- Best fitness value
- Best distance
- Plots for fitness history, distance history, and the route map

## Project Structure

```
genetic-tsp-solver/
│
├─ data/                # Folder for TSP datasets
├─ genetic.py           # Genetic Algorithm implementation
├─ main.py              # Script to run GA on a dataset
├─ utils.py             # Helper functions (distance, fitness, plotting)
└─ README.md            # Project documentation
```
- Soft clauses: start with SOFT_CLAUSE, followed by literals, ending with weight
- Literals can be variables (e.g., x1) or negations (e.g., ~x2)

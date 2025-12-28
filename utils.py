
import matplotlib.pyplot as plt
import random
from typing import List, Tuple


def read_dataset(filename: str) -> List[Tuple[float, float]]:
    with open("./data/" + filename + ".tsp", 'r') as f:
        cities: List[Tuple[float, float]] = []
        for line in f:
            parts = line.split()
            if len(parts) == 3 and ":" not in parts:
                cities.append((float(parts[1]), float(parts[2])))
    return cities


def create_distance_matrix(cities: List[Tuple[float, float]]) -> List[List[float]]:
    distance = lambda x, y: ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** (1/2)
    distance_matrix: List[List[float]] = []

    for i in range(len(cities)):
        distance_matrix.append([])
        for j in range(len(cities)):
            distance_matrix[i].append(distance(cities[i], cities[j]))

    return distance_matrix


def calculate_route_distance(route: List[int], distance_matrix: List[List[float]]) -> float:
    tour_length = 0
    for i in range(len(route) - 1):
        tour_length += distance_matrix[route[i]][route[i+1]]
    
    return tour_length


def fitness(route: List[int], distance_matrix: List[List[float]]) -> float:
    _fitness = 1 / calculate_route_distance(route, distance_matrix)
    return _fitness
   

def generate_initial_population(num_individuals: int, num_cities: int) -> List[List[int]]:
    initial_population = [random.sample(range(num_cities), num_cities) for _ in range(num_individuals)]
    return initial_population


def plot_route(cities, route=None):
    plt.figure(figsize=(10, 6))
    
    if route is not None:
        for i in range(len(route)):
            start = cities[route[i]]
            end   = cities[route[(i + 1) % len(route)]]
            plt.plot([start[0], end[0]], [start[1], end[1]], 'r-')

        # Highlight start and end nodes
        start_node = cities[route[0]]
        end_node   = cities[route[-1]]
        plt.scatter(*start_node, c='green', s=150, marker='*', label='Start')
        # plt.text(start_node[0] + 0.1, start_node[1] + 0.02, "Start", fontsize=9, color='green')
        
        plt.scatter(*end_node, c='red', s=150, marker='X', label='End')
        # plt.text(end_node[0] + 0.1, end_node[1] + 0.02, "End", fontsize=9, color='red')

    # Plot all cities and their indices
    xs = [pt[0] for pt in cities]
    ys = [pt[1] for pt in cities]
    plt.scatter(xs, ys, c='blue', marker='o')
    for i, (x, y) in enumerate(cities):
        plt.text(x + 0.02, y + 0.02, str(i), fontsize=9, color='black')

    plt.title("2D Map of Points")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.legend()
    plt.show()

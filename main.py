
from genetic import GeneticAlgorithm
from utils import generate_initial_population, create_distance_matrix, plot_route,read_dataset,fitness
import matplotlib.pyplot as plt


# TSP problem parameters

CITY_COORDINATES = read_dataset("dj38")

NUM_CITIES = len(CITY_COORDINATES)

def main():
    distance_matrix = create_distance_matrix(CITY_COORDINATES)
    population = generate_initial_population(num_individuals=200, num_cities=NUM_CITIES)
    fitness_func = lambda route: fitness(route, distance_matrix)

    ga = GeneticAlgorithm(population, fitness_func,
                          num_generations=600,
                          mutation_rate=0.1,
                          crossover_rate=0.9,
                          tournament_size=3)
    
    
    best_route, best_fitness,fitness_hist,distance_hist = ga.run()
    print("Best route found:", best_route,len(best_route))
    print("Best fitness found:", best_fitness)
    print("Best distance found:", 1/best_fitness)
    plt.plot(fitness_hist, label='Fitness History')
    plt.xlabel('Generation')
    plt.ylabel('Value')
    plt.title('Fitness History')
    plt.legend()
    plt.show()

    plt.plot(distance_hist, label='Distance History')
    plt.xlabel('Generation')
    plt.ylabel('Value')
    plt.title('distance History')
    plt.legend()
    plt.show()
    plot_route(CITY_COORDINATES, best_route)

if __name__ == '__main__':
    main()

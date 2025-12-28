import random
from typing import List, Callable, Tuple
from utils import create_distance_matrix, calculate_route_distance, fitness


class GeneticAlgorithm:
    def __init__(
        self,
        population: List[List[int]],
        fitness_func: Callable[[List[int]], float],
        num_generations: int = 100,
        mutation_rate: float = 0.05,
        crossover_rate: float = 0.8,
        selection_strategy: str = 'tournament',  # 'tournament', 'roulette', 'rank'
        crossover_strategy: str = 'order crossover',  # 'one_point', 'two_point', 'uniform'
        mutation_strategy: str = 'swap',        # 'swap', 'inversion', 'scramble'
        tournament_size: int = 3,
    ) -> None:
       
        self.population: List[List[int]] = population
        self.fitness_func: Callable[[List[int]], float] = fitness_func
        self.num_generations: int = num_generations
        self.mutation_rate: float = mutation_rate
        self.crossover_rate: float = crossover_rate
        self.selection_strategy: str = selection_strategy
        self.crossover_strategy: str = crossover_strategy
        self.mutation_strategy: str = mutation_strategy
        self.tournament_size: int = tournament_size

        self.best_fitness_history: List[float] = []
        self.best_distance_history: List[float] = []

    def evaluate_population(self) -> List[float]:
        fitness_rates = []

        for route in self.population:
            _fitness = self.fitness_func(route)
            fitness_rates.append(_fitness)
        
        return fitness_rates
    

    def selection(self, fitnesses: List[float]) -> int:
        if self.selection_strategy == "roulette":
            min_f = min(fitnesses)
            max_f = max(fitnesses)
            if max_f == min_f:
                rates = [1.0] * len(fitnesses)
            else:
                rates = [(f - min_f) / (max_f - min_f) + 0.1 for f in fitnesses]  

        elif self.selection_strategy == "rank":
            rates = sorted(range(len(fitnesses)), key=lambda i: fitnesses[i])
                    
        elif self.selection_strategy == "tournament":
            indices = random.sample(range(len(fitnesses)), self.tournament_size)

            _max = 0, 0
            for index in indices:
                if fitnesses[index] > _max[0]:
                    _max = fitnesses[index], index
            
            return _max[1]
        else:
            return random.randint(0, len(fitnesses) - 1)
        
        if self.selection_strategy == "roulette" or self.selection_strategy == "rank":
            total_sum = sum(rates)
            cum_sum = 0
            threshold = random.uniform(0, total_sum)

            for i in range(len(rates)):
                cum_sum += rates[i]
                if cum_sum > threshold:
                    return i   


    def crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        do_crossover = random.uniform(0, 1) < self.crossover_rate
        if not do_crossover:
            return [parent1, parent2]
        
        cities_num = len(parent1)
        child1 = [None] * cities_num
        child2 = [None] * cities_num

        if self.crossover_strategy == "order crossover":
            crs_num1 = random.randint(0, cities_num - 1)
            crs_num2 = random.randint(0, cities_num - 1)

            if crs_num1 > crs_num2:
                crs_num1, crs_num2 = crs_num2, crs_num1
            
            partition_1 = parent1[crs_num1:crs_num2]
            i = 0
            child1[crs_num1: crs_num2] = partition_1
            for state in parent2:
                if i == crs_num1:
                    i = crs_num2
                if not (state in partition_1):
                    child1[i] = state
                    i += 1

            partition_2 = parent2[crs_num1:crs_num2]
            i = 0
            child2[crs_num1: crs_num2] = partition_2
            for state in parent1:
                if i == crs_num1:
                    i = crs_num2
                if not (state in partition_2):
                    child2[i] = state
                    i += 1


        elif self.crossover_strategy == "one_point":
            crs_num = random.randint(0, cities_num - 1)
            child1 = parent1[:crs_num] + parent2[crs_num:]
            child2 = parent2[:crs_num] + parent1[crs_num:]
        
        elif self.crossover_strategy == "two_point":
            crs_num1 = random.randint(0, cities_num - 1)
            crs_num2 = random.randint(0, cities_num - 1)

            if crs_num1 > crs_num2:
                crs_num1, crs_num2 = crs_num2, crs_num1

            child1 = parent1[:crs_num1] + parent2[crs_num1:crs_num2] + parent1[crs_num2:]
            child2 = parent2[:crs_num1] + parent1[crs_num1:crs_num2] + parent2[crs_num2:]
        
        elif self.crossover_strategy == "uniform":
            mask = [random.randint(0, 1) for _ in range(cities_num)]
            child1 = [parent1[i] if mask[i] else parent2[i] for i in range(cities_num)]
            child2 = [parent2[i] if mask[i] else parent1[i] for i in range(cities_num)]
        
        return [child1, child2]
        

    def mutation(self, individual: List[int]) -> List[int]:
        do_mutation = random.uniform(0, 1) < self.mutation_rate
        if not do_mutation:
            return individual
        
        index_1, index_2 = random.randint(0, len(individual) - 1), random.randint(0, len(individual) - 1)
        new_ind = individual.copy()

        if index_2 < index_1:
            index_1, index_2 = index_2, index_1

        if self.mutation_strategy == "swap":
            new_ind[index_1], new_ind[index_2] = individual[index_2], individual[index_1]
        
        elif self.mutation_strategy == "inversion":
            new_ind[index_1:index_2] = list(reversed(individual[index_1: index_2]))
        
        elif self.mutation_strategy == "scramble":
            new_ind[index_1:index_2] = random.sample(new_ind[index_1: index_2], index_2 - index_1)
        
        return new_ind
        
        
    def run(self) -> Tuple[List[int], float, List[float], List[float]]:
        num_individuals = len(self.population)
        for _ in range(self.num_generations):

            fitnesses = self.evaluate_population()
            best_fit = max(fitnesses)
            best_dist = 1 / best_fit # Knowing that the fitness function is the inverse of distance

            self.best_fitness_history.append(best_fit)
            self.best_distance_history.append(best_dist)


            next_gen = [self.population[self.selection(fitnesses)] for _ in range(num_individuals)]
            for i in range(0, num_individuals, 2):
                next_gen[i], next_gen[i + 1] = self.crossover(next_gen[i], next_gen[i + 1])
                next_gen[i] = self.mutation(next_gen[i])
                next_gen[i + 1] = self.mutation(next_gen[i + 1])
            
            self.population = next_gen
            next_gen = []
        
        fitnesses = self.evaluate_population()
        route_fit = list(zip(self.population, fitnesses))

        best_route, best_fit = max(route_fit, key=lambda x: x[1])

        return best_route, best_fit, self.best_fitness_history ,self.best_distance_history


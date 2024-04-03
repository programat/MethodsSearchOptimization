import random

class GeneticAlgorithm:
    def __init__(self, fitness_func, population_size, num_generations, mutation_rate, survival_rate):
        self.fitness_func = fitness_func
        self.population_size = population_size
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate
        self.survival_rate = survival_rate
        self.population = []

    def initialize_population(self, x_bounds, y_bounds):
        self.population = [self.create_individual(x_bounds, y_bounds) for _ in range(self.population_size)]

    def create_individual(self, x_bounds, y_bounds):
        x_min, x_max = x_bounds
        y_min, y_max = y_bounds
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        fitness = self.fitness_func(x, y)
        return [x, y, fitness]

    def selection(self):
        sorted_population = sorted(self.population, key=lambda ind: ind[2])
        num_survivors = int(self.population_size * self.survival_rate)
        survivors = sorted_population[:num_survivors]
        self.population = survivors + self.create_offspring(survivors)

    def create_offspring(self, parents):
        offspring = []
        num_offspring = self.population_size - len(parents)
        for _ in range(num_offspring):
            parent1, parent2 = random.sample(parents, 2)
            child = self.crossover(parent1, parent2)
            offspring.append(child)
        return offspring

    def crossover(self, parent1, parent2):
        x = random.choice([parent1[0], parent2[0]])
        y = random.choice([parent1[1], parent2[1]])
        fitness = self.fitness_func(x, y)
        return [x, y, fitness]

    def mutation(self):
        for individual in self.population:
            if random.random() < self.mutation_rate:
                individual[0] += random.gauss(0, 0.1)
            if random.random() < self.mutation_rate:
                individual[1] += random.gauss(0, 0.1)
            individual[2] = self.fitness_func(individual[0], individual[1])

    def run(self, x_bounds, y_bounds):
        self.initialize_population(x_bounds, y_bounds)
        for generation in range(self.num_generations):
            self.selection()
            self.mutation()
            yield self.population
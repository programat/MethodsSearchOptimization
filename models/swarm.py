import numpy as np


class Particle:
    def __init__(self, dim, min_bound, max_bound):
        self.position = np.random.uniform(min_bound, max_bound, dim)
        self.velocity = np.zeros(dim)
        self.best_position = self.position.copy()
        self.best_fitness = float('inf')

    def update_velocity(self, global_best_position, w, c1, c2):
        r1 = np.random.rand(len(self.position))
        r2 = np.random.rand(len(self.position))
        cognitive_velocity = c1 * r1 * (self.best_position - self.position)
        social_velocity = c2 * r2 * (global_best_position - self.position)
        self.velocity = w * self.velocity + cognitive_velocity + social_velocity

    def update_position(self, min_bound, max_bound):
        self.position = self.position + self.velocity
        self.position = np.clip(self.position, min_bound, max_bound)


class PSO:
    def __init__(self, fitness_func, dim, min_bound, max_bound, swarm_size=100,
                 w=0.729, c1=1.49, c2=1.49):
        self.fitness_func = fitness_func
        self.dim = dim
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.swarm_size = swarm_size
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.swarm = [Particle(dim, min_bound, max_bound) for _ in range(swarm_size)]
        self.global_best_position = np.zeros(dim)
        self.global_best_fitness = float('inf')

    def run(self, max_iter):
        for i in range(max_iter):
            for particle in self.swarm:
                fitness = self.fitness_func(*particle.position)
                if fitness < particle.best_fitness:
                    particle.best_fitness = fitness
                    particle.best_position = particle.position.copy()
                if fitness < self.global_best_fitness:
                    self.global_best_fitness = fitness
                    self.global_best_position = particle.position.copy()

            for particle in self.swarm:
                particle.update_velocity(self.global_best_position, self.w, self.c1, self.c2)
                particle.update_position(self.min_bound, self.max_bound)

            positions = [[p.position[0], p.position[1], self.fitness_func(*p.position)] for p in self.swarm]
            best_positions = [[p.best_position[0], p.best_position[1], p.best_fitness] for p in self.swarm]

            yield positions, best_positions, self.global_best_position, self.global_best_fitness
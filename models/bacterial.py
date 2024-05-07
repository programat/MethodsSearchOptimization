import numpy as np


class Bacterial:
    def __init__(self, func, num_bacteria, num_chemotactic, num_elimination, position_x=5, position_y=5):
        self.func = func
        self.pos_x = float(position_x)
        self.pos_y = float(position_y)
        self.num_bacteria = int(num_bacteria)
        self.agents = np.random.uniform(-self.pos_x, self.pos_x, (self.num_bacteria, 2))
        self.agents = np.hstack((self.agents, np.zeros((self.num_bacteria, 2))))
        for i in range(self.num_bacteria):
            self.agents[i, 2] = self.func(self.agents[i, 0], self.agents[i, 1])
            self.agents[i, 3] = self.agents[i, 2]
        self.num_chemotactic = num_chemotactic
        self.num_elimination = num_elimination

    def run(self, iter_count):
        for i in range(iter_count):
            self.chemotaxis(1 / (i + 1))
            self.reproduction()
            self.elimination()
            best_position = self.get_best()
            yield self.agents[:, :3], best_position[:3]

    def chemotaxis(self, coef):
        vec = np.random.uniform(-1, 1, (self.num_bacteria, 2)) * coef
        for _ in range(self.num_chemotactic):
            self.agents[:, :2] += vec
            self.agents[:, 2] = self.func(self.agents[:, 0], self.agents[:, 1])
            self.agents[:, 3] += self.agents[:, 2]
            mask = self.agents[:, 2] < self.agents[:, 3]
            vec[mask] = np.random.uniform(-1, 1, (np.sum(mask), 2)) * coef

    def reproduction(self):
        self.agents = self.agents[np.argsort(self.agents[:, 3])]
        self.agents[self.num_bacteria // 2:, :] = self.agents[:self.num_bacteria // 2, :]

    def elimination(self):
        mask = np.random.rand(self.num_bacteria) <= self.num_elimination
        self.agents[mask, :2] = np.random.uniform(-self.pos_x, self.pos_x, (np.sum(mask), 2))
        self.agents[mask, 2] = self.func(self.agents[mask, 0], self.agents[mask, 1])
        self.agents[mask, 3] = self.agents[mask, 2]

    def get_best(self):
        return self.agents[np.argmin(self.agents[:, 2])]


if __name__ == '__main__':
    from models.functions import SphereFunction
    func = SphereFunction()
    # Пример использования
    bacterial = Bacterial(func=func.get_function_point, num_bacteria=50, num_chemotactic=100, num_elimination=2)

    for iteration, (points, best_position) in enumerate(bacterial.run(iter_count=10)):
        print(f"Iteration {iteration + 1}:")
        print("Points:")
        print(points)
        print(f"Best position: {best_position}")
        # print(f"Best fitness: {best_fitness}")
        print()
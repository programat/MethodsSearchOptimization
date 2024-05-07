import random
from operator import itemgetter


class Bacterial:
    def __init__(self, func, num_bacteria, num_chemotactic, step_elimination, position_x=5, position_y=5):
        self.func = func
        self.pos_x = float(position_x)
        self.pos_y = float(position_y)
        self.num_bacteria = int(num_bacteria)
        self.agents = [[random.uniform(-self.pos_x, self.pos_x), random.uniform(-self.pos_y, self.pos_y), 0.0, 0.0] for
                       _ in range(self.num_bacteria)]

        for i in self.agents:
            i[2] = self.func(i[0], i[1])
            i[3] = i[2]

        self.num_chemotactic = num_chemotactic
        self.step_elimination = step_elimination

    def chemotaxis(self, coef):
        for bac in self.agents:
            vec = [coef * random.uniform(-1, 1), coef * random.uniform(-1, 1)]
            for _ in range(self.num_chemotactic):
                f = bac[2]

                bac[0] += vec[0]  # X
                bac[1] += vec[1]  # Y
                bac[2] = self.func(bac[0], bac[1])  # Z / Fitness Function
                bac[3] += bac[2]  # Health

                if f < bac[2]:
                    vec = [coef * random.uniform(-1, 1), coef * random.uniform(-1, 1)]

    def reproduction(self):
        self.agents = sorted(self.agents, key=itemgetter(3), reverse=False)
        for i in range(self.num_bacteria // 2):
            self.agents[self.num_bacteria // 2 + i] = self.agents[i].copy()

    def elimination(self):
        for bac in self.agents:
            if random.uniform(0, 1) <= self.step_elimination:
                bac[0] = random.uniform(-self.pos_x, self.pos_x)
                bac[1] = random.uniform(-self.pos_y, self.pos_y)
                bac[2] = self.func(bac[0], bac[1])
                bac[3] = bac[2]

    def get_best(self):
        return sorted(self.agents, key=itemgetter(2), reverse=False)[0]

    def run(self, iter_count):
        for i in range(iter_count):
            self.chemotaxis(1 / (i + 1))
            self.reproduction()
            self.elimination()

            yield self.agents, self.get_best()
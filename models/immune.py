import numpy as np


class Immune:
    def __init__(self, func, pop_size, num_best, num_clones, num_best_clones, mutation_rate, bounds):
        self.func = func
        self.pop_size = pop_size
        self.num_best = num_best
        self.num_clones = num_clones
        self.num_best_clones = num_best_clones
        self.mutation_rate = mutation_rate
        self.bounds = bounds

        # Инициализация популяции антител
        self.antibodies = np.random.uniform(bounds[0], bounds[1], size=(pop_size, 2))

    def affinity(self, antibody):
        x, y = antibody
        return -self.func(x, y)

    def mutate(self, antibody):
        return antibody + self.mutation_rate * np.random.uniform(-0.5, 0.5, size=antibody.shape)

    def run(self, num_iterations):
        for iteration in range(num_iterations):
            # Вычисление аффинности антител
            affinities = np.array([self.affinity(antibody) for antibody in self.antibodies])

            # Клональная селекция и соматическая гипермутация:
            # Выбор лучших антител
            best_indices = np.argsort(affinities)[-self.num_best:]
            best_antibodies = self.antibodies[best_indices]
            # Клонирование и мутация лучших антител
            clones = np.repeat(best_antibodies, self.num_clones, axis=0)
            mutated_clones = np.array([self.mutate(clone) for clone in clones])

            # Вычисление аффинности клонов
            clone_affinities = np.array([self.affinity(clone) for clone in mutated_clones])

            # Выбор лучших клонов
            best_clone_indices = np.argsort(clone_affinities)[-self.num_best_clones:]
            best_clones = mutated_clones[best_clone_indices]

            # Объединение популяции антител с лучшими клонами
            self.antibodies = np.vstack((self.antibodies, best_clones))

            # Сжатие популяции антител
            affinities = np.array([self.affinity(antibody) for antibody in self.antibodies])
            best_indices = np.argsort(affinities)[-self.pop_size:]
            self.antibodies = self.antibodies[best_indices]

            # Обновление массива affinities после сжатия популяции
            affinities = affinities[best_indices]

            # Вывод информации на текущей итерации
            best_antibody = self.antibodies[np.argmax(affinities)]
            yield self.antibodies, best_antibody

        # Возвращение лучшего решения
        # best_antibody = self.antibodies[np.argmax(affinities)]
        # return best_antibody
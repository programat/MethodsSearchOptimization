import traceback

import numpy as np

from models.generations import GeneticAlgorithm
from models.swarm import PSO


def hybrid_algorithm(fitness_func, dim, min_bound, max_bound, ga_generations, pso_iterations,
                     ga_population_size, ga_mutation_rate, ga_survival_rate,
                     pso_swarm_size, pso_w, pso_c1, pso_c2):
    # Запуск генетического алгоритма
    ga = GeneticAlgorithm(fitness_func, population_size=ga_population_size, num_generations=ga_generations,
                          mutation_rate=ga_mutation_rate, survival_rate=ga_survival_rate)
    for i, population in enumerate(ga.run((min_bound, max_bound), (min_bound, max_bound))):
        yield f"GA Generation {i}:", population

    # Получение лучшего решения из генетического алгоритма
    best_solution = min(population, key=lambda ind: ind[2])

    # Запуск алгоритма роя частиц, начиная с лучшего решения GA
    pso = PSO(fitness_func, dim, min_bound, max_bound, swarm_size=pso_swarm_size, w=pso_w, c1=pso_c1, c2=pso_c2)
    pso.global_best_position = np.array(best_solution[:2])
    pso.global_best_fitness = best_solution[2]

    for i, (positions, best_positions, global_best_position, global_best_fitness) in enumerate(pso.run(pso_iterations)):
        yield f"PSO Iteration {i}:", positions, best_positions, global_best_position, global_best_fitness


class Lab8Controller:
    def __init__(self, window):
        self.window = window
        self.function = None

        # lab3
        self.popul_count = None
        self.gen_count = None
        self.surv = None
        self.mut_chance = None

        # lab4
        self.swarm_count = None
        self.iter_count = None
        self.c1_coef = None
        self.c2_coef = None
        self.inertia = None

    def popul_count_getter(self):
        self.popul_count = self.window.pop_size_lab8.text()
        return self.popul_count

    def gen_count_getter(self):
        self.gen_count = self.window.gen_count_lab8.text()
        return self.gen_count

    def surv_getter(self):
        self.surv = self.window.surv_chance_lab8.text()
        return self.surv

    def mut_chance_getter(self):
        self.mut_chance = self.window.mut_chance_lab8.text()
        return self.mut_chance

    def swarm_count_getter(self):
        self.swarm_count = self.window.part_count_lab8.text()
        return self.swarm_count

    def iter_count_getter(self):
        self.iter_count = self.window.part_iter_count_lab8.text()
        return self.iter_count

    def c1_coef_getter(self):
        self.c1_coef = self.window.c1_coef_lab8.text()
        return self.c1_coef

    def c2_coef_getter(self):
        self.c2_coef = self.window.c2_coef_lab8.text()
        return self.c2_coef

    def inertia_getter(self):
        self.inertia = self.window.iner_coef_lab8.text()
        return self.inertia

    def onStartButtonClicked(self):
        self.start_calc()

    def set_function(self, function):
        self.function = function

    def delay_getter(self):
        delay = self.window.delay_lab8.text()
        if delay.replace(' ', '') != '' or float(delay) in range(0, 10):
            return float(delay)
        return 0.1

    def start_calc(self):
        # lab3
        self.popul_count_getter()
        self.gen_count_getter()
        self.surv_getter()
        self.mut_chance_getter()
        
        # lab4
        self.swarm_count_getter()
        self.iter_count_getter()
        self.c1_coef_getter()
        self.c2_coef_getter()
        self.inertia_getter()

        try:
            # lab3
            self.popul_count = int(self.popul_count)
            self.gen_count = int(self.gen_count)
            self.surv = float(self.surv_getter())
            self.mut_chance = float(self.mut_chance_getter())

            # lab4
            self.swarm_size = int(self.swarm_count_getter())
            self.iter_count = int(self.iter_count_getter())
            self.c1_coef = float(self.c1_coef_getter())
            self.c2_coef = float(self.c2_coef_getter())
            self.inertia = float(self.inertia_getter())

            delay = float(self.delay_getter())

            x_bounds = (-5, 5)
            y_bounds = (-5, 5)
            allPoints = []

            for step in hybrid_algorithm(self.function.get_function_point, 2, -5, 5,
                                         self.gen_count, self.iter_count,
                                         self.popul_count, self.mut_chance, self.surv,
                                         self.swarm_size, self.inertia, self.c1_coef, self.c2_coef):
                # algorithm, data = step
                if len(step) == 2:
                    algorithm, population = step
                    points = [[individual[0], individual[1], self.function.get_function_point(*individual[:2])]
                              for individual in population]
                    allPoints.append(points)
                    min_point = min(points, key=lambda x: x[2])
                    self.window.updateText(
                        f'{algorithm}: Best point: {min_point[0]:.3f}, {min_point[1]:.3f}, f: {min_point[2]:.3f}',
                        delay=delay)
                else:
                    algorithm, positions, best_positions, global_best_position, global_best_fitness = step
                    points = [[p[0], p[1], self.function.get_function_point(*p[:2])] for p in positions]
                    allPoints.append(points)
                    self.window.updateText(
                        f'{algorithm}: Best point: {global_best_position[0]:.3f}, {global_best_position[1]:.3f}, f: {global_best_fitness:.3f}',
                        delay=delay)

            self.window.updateListPoint(allPoints, marker='.', delay=delay)
            self.window.textOutput.clear()

        except TypeError or ValueError as ex:
            print(traceback.format_exc())

            self.window.textOutput.clear()

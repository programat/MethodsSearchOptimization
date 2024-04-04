import traceback

from models.swarm import PSO
from models.functions import SphereFunction

class Lab4Controller:
    def __init__(self, window):
        self.window = window
        self.function = SphereFunction()
        self.swarm_count = None
        self.iter_count = None
        self.c1_coef = None
        self.c2_coef = None
        self.inertia = None

    def swarm_count_getter(self):
        self.swarm_count = self.window.swarm_count.text()
        return self.swarm_count

    def iter_count_getter(self):
        self.iter_count = self.window.iter_count2.text()
        return self.iter_count

    def c1_coef_getter(self):
        self.c1_coef = self.window.c1_coef.text()
        return self.c1_coef

    def c2_coef_getter(self):
        self.c2_coef = self.window.c2_coef.text()
        return self.c2_coef

    def inertia_getter(self):
        self.inertia = self.window.inertia.text()
        return self.inertia

    def onStartButtonClicked(self):
        self.start_calc()

    def delay_getter(self):
        delay = self.window.lab4_delay.text()
        if delay.replace(' ', '') != '' or float(delay) in range(0, 10):
            return float(delay)
        return 0.1

    def start_calc(self):
        self.swarm_count_getter()
        self.iter_count_getter()
        self.c1_coef_getter()
        self.c2_coef_getter()
        self.inertia_getter()
        try:
            self.swarm_size = int(self.swarm_count_getter())
            self.iter_count = int(self.iter_count_getter())
            self.c1_coef = float(self.c1_coef_getter())
            self.c2_coef = float(self.c2_coef_getter())
            self.inertia = float(self.inertia_getter())
            delay = float(self.delay_getter())

            self.window.textOutput.clear()
            pso = PSO(self.function.get_function_point, dim=2, min_bound=-5, max_bound=5,
                      swarm_size=self.swarm_size, w=self.inertia, c1=self.c1_coef, c2=self.c2_coef)

            allPoints = []
            allBestPoints = []

            for i, (positions, best_positions, global_best_position, global_best_fitness) in enumerate(pso.run(self.iter_count)):
                allPoints.append(positions)
                allBestPoints.append(best_positions)

                self.window.updateText(f'Iteration {i}: Best fitness: {global_best_fitness:.5f}', delay=delay)

            self.window.updateListPoint(allPoints, marker='.', delay=delay)
            self.window.updateListPoint(allBestPoints, marker='o', delay=delay)

        except TypeError or ValueError:
            print(traceback.format_exc())
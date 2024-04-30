import traceback

from models.generations import GeneticAlgorithm
from models.gradient import Gradient
from models.functions import RosenbrockFunction

class Lab3Controller:
    def __init__(self, window):
        self.window = window
        self.function = RosenbrockFunction()
        self.popul_count = None
        self.gen_count = None
        self.surv = None
        self.mut_chance = None

    def popul_count_getter(self):
        self.popul_count = self.window.popul_count.text()
        return self.popul_count

    def gen_count_getter(self):
        self.gen_count = self.window.gen_count.text()
        return self.gen_count

    def surv_getter(self):
        self.surv = self.window.surv.text()
        return self.surv

    def mut_chance_getter(self):
        self.mut_chance = self.window.mut_chance.text()
        return self.mut_chance

    def onStartButtonClicked(self):
        self.start_calc()

    def delay_getter(self):
        delay = self.window.lab3_delay.text()
        if delay.replace(' ', '') != '' or float(delay) in range(0, 10):
            return float(delay)
        return 0.1

    def start_calc(self):
        self.popul_count_getter()
        self.gen_count_getter()
        self.surv_getter()
        self.mut_chance_getter()
        try:
            self.popul_count = int(self.popul_count)
            self.gen_count = int(self.gen_count)
            self.surv = float(self.surv_getter())
            self.mut_chance = float(self.mut_chance_getter())
            delay = float(self.delay_getter())

            self.window.textOutput.clear()
            genetic_algorithm = GeneticAlgorithm(self.function.get_function_point, self.popul_count, self.gen_count, self.mut_chance,
                                                 self.surv)

            x_bounds = (-5, 5)
            y_bounds = (-5, 5)

            allPoints = []

            for i, population in enumerate(genetic_algorithm.run(x_bounds, y_bounds)):
                # self.window.graph.clear_points()
                points = []
                for individual in population:
                    x, y, _ = individual
                    points.append([x, y, self.function.get_function_point(x, y)])

                allPoints.append(points)

                min_point = [round(i, 3) for i in min(points, key=lambda x: x[2])]
                self.window.updateText(f'{i}: Best point: {min_point[0], min_point[1]}, f: {min_point[2]}', delay=delay)

            # print(allPoints)
            self.window.updateListPoint(allPoints, marker='.', delay=delay)



            # best_individual = min(population, key=lambda ind: ind[2])
            # self.window.updatePoint([[best_individual[0], best_individual[1], best_individual[2]]], color='red', marker='*')

        except TypeError or ValueError as ex:
            print(traceback.format_exc())


            # for population in genetic_algorithm.run(x_bounds, y_bounds):
            #     # self.window.graph.clear_points()
            #     points = []
            #     for individual ibfn population:
            #         x, y, _ = individual
            #         points.append([x, y, self.function.get_function_point(x, y)])
            #
            #     allPoints.append(points)
            #
            # i = 0
            # while (True):
            #     if (not self.window.point_list_thread.painting):
            #         self.window.graph.clear_points()
            #         self.window.updateListPoint(allPoints[i], marker='.', delay=.1)
            #         i = i + 1
            #     if (i == len(allPoints)):
            #         break
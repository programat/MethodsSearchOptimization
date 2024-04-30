import traceback

from models.bees import Bees


class Lab5Controller:
    def __init__(self, window):
        self.window = window
        self.function = None
        self.iter_count = None
        self.scout_count = None
        self.bee_in_pers_count = None
        self.bee_in_best_count = None
        self.pers_count = None
        self.elite_count = None
        self.dist_size = None


    def iter_count_getter(self):
        self.iter_count = self.window.iter_count_lab5.text()
        return self.iter_count

    def scout_count_getter(self):
        self.scout_count = self.window.scout_count.text()
        return self.scout_count

    def bee_in_pers_count_getter(self):
        self.bee_in_pers_count = self.window.bee_in_pers_count.text()
        return self.bee_in_pers_count

    def bee_in_best_count_getter(self):
        self.bee_in_best_count = self.window.bee_in_best_count.text()
        return self.bee_in_best_count

    def pers_count_getter(self):
        self.pers_count = self.window.pers_count.text()
        return self.pers_count

    def elite_count_getter(self):
        self.elite_count = self.window.elite_count.text()
        return self.elite_count

    def dist_size_getter(self):
        self.dist_size = self.window.dist_size.text()
        return self.dist_size

    def onStartButtonClicked(self):
        self.start_calc()

    def set_function(self, function):
        self.function = function

    def delay_getter(self):
        delay = self.window.lab5_delay.text()
        if delay.replace(' ', '') != '' or float(delay) in range(0, 10):
            return float(delay)
        return 0.1

    def start_calc(self):
        self.iter_count_getter()
        self.scout_count_getter()
        self.bee_in_pers_count_getter()
        self.bee_in_best_count_getter()
        self.pers_count_getter()
        self.elite_count_getter()
        self.dist_size_getter()
        self.delay_getter()
        try:
            self.iter_count = int(self.iter_count)
            self.scout_count = int(self.scout_count)
            self.bee_in_pers_count = int(self.bee_in_pers_count)
            self.bee_in_best_count = int(self.bee_in_best_count)
            self.pers_count = int(self.pers_count)
            self.elite_count = int(self.elite_count)
            self.dist_size = float(self.dist_size)
            delay = float(self.delay_getter())

            self.window.textOutput.clear()
            bees = Bees(self.function.get_function_point, self.scout_count, self.elite_count, self.pers_count,
                        self.bee_in_best_count, self.bee_in_pers_count, self.dist_size, 5, 5)

            all_points = []

            for i, (bees_data, selected_data, best_bee) in enumerate(bees.run(self.iter_count)):
                points = []
                for mielpops in bees_data:
                    x, y, z = mielpops
                    points.append([x, y, z])

                all_points.append(points)

                best_x, best_y, best_fitness = best_bee
                self.window.updateText(f"Iteration {i}: Best solution: ({best_x: .5f}, {best_y: .5f}, {best_fitness: .5f})", delay=delay)

            # print(allPoints)
            self.window.updateListPoint(all_points, marker='.', delay=delay)

        except TypeError or ValueError as _:
            print(traceback.format_exc())

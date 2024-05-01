import traceback

from models.immune import Immune


class Lab6Controller:
    def __init__(self, window):
        self.window = window
        self.function = None
        self.iter_count = None
        self.rand_antbd_count = None
        self.antibody_count_lab6 = None
        self.best_antbd_count = None
        self.clone_count = None
        self.mut_coef_lab6 = None


    def iter_count_getter(self):
        self.iter_count = self.window.iter_count_lab6.text()
        return self.iter_count

    def rand_antbd_count_getter(self):
        self.rand_antbd_count = self.window.rand_antbd_count.text()
        return self.rand_antbd_count

    def antibody_count_lab6_getter(self):
        self.antibody_count_lab6 = self.window.antibody_count_lab6.text()
        return self.antibody_count_lab6
    
    def best_antbd_count_getter(self):
        self.best_antbd_count = self.window.best_antbd_count.text()
        return self.best_antbd_count
    
    def clone_count_getter(self):
        self.clone_count = self.window.clone_count.text()
        return self.clone_count

    def mut_coef_lab6_getter(self):
        self.mut_coef_lab6 = self.window.mut_coef_lab6.text()
        return self.mut_coef_lab6

    def onStartButtonClicked(self):
        self.start_calc()

    def set_function(self, function):
        self.function = function

    def delay_getter(self):
        delay = self.window.lab6_delay.text()
        if delay.replace(' ', '') != '' or float(delay) in range(0, 10):
            return float(delay)
        return 0.1

    def start_calc(self):
        self.iter_count_getter()
        self.rand_antbd_count_getter()
        self.antibody_count_lab6_getter()
        self.best_antbd_count_getter()
        self.clone_count_getter()
        self.mut_coef_lab6_getter()
        self.delay_getter()
        try:
            self.iter_count = int(self.iter_count)
            self.rand_antbd_count = int(self.rand_antbd_count)
            self.antibody_count_lab6 = int(self.antibody_count_lab6)
            self.best_antbd_count = int(self.best_antbd_count)
            self.clone_count = int(self.clone_count)
            self.mut_coef_lab6 = float(self.mut_coef_lab6)

            delay = float(self.delay_getter())

            self.window.textOutput.clear()
            immune = Immune(func=self.function.get_function_point, pop_size=self.antibody_count_lab6, num_clones=self.clone_count,
                              num_best=self.best_antbd_count, num_best_clones=self.rand_antbd_count, bounds=(5,5), mutation_rate=self.mut_coef_lab6)

            all_points = []

            for i, (antibodies, best_antibody) in enumerate(immune.run(self.iter_count)):
                print(antibodies)
                points = []
                for ameba in antibodies:
                    x, y = ameba
                    points.append([x, y, self.function.get_function_point(x,y)])

                all_points.append(points)

                best_x, best_y = best_antibody
                self.window.updateText(f"Iteration {i}: Best solution: ({best_x: .5f}, {best_y: .5f}, {self.function.get_function_point(best_x,best_y): .5f})", delay=delay)

            # print(allPoints)
            self.window.updateListPoint(all_points, marker='.', delay=delay)

        except TypeError or ValueError as _:
            print(traceback.format_exc())

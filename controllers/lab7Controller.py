import traceback

from models.bacterial import Bacterial


class Lab7Controller:
    def __init__(self, window):
        self.window = window
        self.function = None
        self.iter_count = None
        self.num_bacteria = None
        self.num_chemotactic = None
        self.num_elimination = None

    def iter_count_getter(self):
        self.iter_count = self.window.iter_count_lab7.text()
        return self.iter_count

    def num_bacteria_getter(self):
        self.num_bacteria = self.window.bacteria_count_lab7.text()
        return self.num_bacteria

    def num_chemotactic_getter(self):
        self.num_chemotactic = self.window.swim_step_count_lab7.text()
        return self.num_chemotactic

    def num_elimination_getter(self):
        self.num_elimination = self.window.liquidation_step_lab7.text()
        return self.num_elimination

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
        self.num_bacteria_getter()
        self.num_chemotactic_getter()
        self.num_elimination_getter()
        self.delay_getter()
        try:
            self.iter_count = int(self.iter_count)
            self.num_bacteria = int(self.num_bacteria)
            self.num_chemotactic = int(self.num_chemotactic)
            self.num_elimination = int(self.num_elimination)

            delay = float(self.delay_getter())

            self.window.textOutput.clear()
            bacterial = Bacterial(func=self.function.get_function_point, num_bacteria=self.num_bacteria, num_chemotactic=self.num_chemotactic, step_elimination=self.num_elimination/100)

            all_points = []

            for i, (bacterias, best_position) in enumerate(bacterial.run(self.iter_count)):
                print(bacterias, end='\n---\n')
                points = []
                for ameba in bacterias:
                    x, y, f, _ = ameba
                    points.append([x, y, f])

                all_points.append(points)

                best_x, best_y, best_func, health = best_position
                self.window.updateText(
                    f"Iteration {i}: Best solution: ({best_x: .5f}, {best_y: .5f}, {best_func: .5f}, health: {health:.5f})",
                    delay=delay)

            # print(allPoints)
            self.window.updateListPoint(all_points, marker='.', delay=delay)

        except TypeError or ValueError as _:
            print(traceback.format_exc())

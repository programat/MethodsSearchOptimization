from models.simplex import Simplex
from models.functions import FunctionLab2


class Lab2Controller:
    def __init__(self, window):
        self.window = window
        self.function = FunctionLab2()
        self.x_start = -5
        self.y_start = -5

    def set_function(self, function):
        pass

    def onStartButtonClicked(self):
        self.start_calc()

    def delay_getter(self):
        delay = self.window.lab2_delay.text()
        if delay.replace(' ', '') != '' or float(delay) in range(0, 10):
            return float(delay)
        return 0.1

    def start_calc(self):
        try:
            arrowHeight = self.window.graph.axes.get_zlim()[1] / 10

            self.window.textOutput.clear()
            simplex = Simplex()
            for i, el in enumerate(simplex.startUp()):
                if i == 0:
                    self.window.updatePoint(*el[:3], color='red', delay=self.delay_getter())
                    self.window.graph.draw_arrow(el[0], el[1], el[2] + arrowHeight, 0, 0, -arrowHeight)
                else:
                    self.window.updatePoint(*el[:3], delay=0.1)

                text = f'{i}:  (x, y, function) = ({round(el[0], 5)}, {round(el[1], 5)}, {round(el[2], 5)})'
                self.window.updateText(text, delay=self.delay_getter())
                point = el[:3]

            self.window.updatePoint(*point, color='green', delay=0.1)
            self.window.graph.draw_arrow(point[0], point[1], point[2] + arrowHeight, 0, 0, -arrowHeight, color='green')

        except TypeError or ValueError as ex:
            print(ex)

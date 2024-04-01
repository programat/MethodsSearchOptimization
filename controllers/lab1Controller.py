import sys
import traceback

from PyQt6.QtCore import pyqtSignal
from PySide6.QtCore import QRunnable

from models.gradient import Gradient

class Lab1Controller:
    def __init__(self, window):
        self.window = window
        self.function = None
        self.x_start = None
        self.y_start = None

    def start_x_getter(self):
        self.x_start = self.window.x_start.text()
        return self.x_start

    def start_y_getter(self):
        self.y_start = self.window.y_start.text()
        return self.y_start

    def start_step_getter(self):
        return self.window.start_step.text()

    def iter_getter(self):
        return self.window.iter_count.text()

    def delay_getter(self):
        return self.window.delay.text()

    def onStartButtonClicked(self):
        self.start_calc()

    def set_function(self, function):
        self.function = function

    def delay_getter(self):
        delay = self.window.lab1_delay.text()
        if delay.replace(' ', '') != '' or float(delay) in range(0, 10):
            return float(delay)
        return 0.1

    # 1-ый питоновский react компонент
    # Егор одобряет!
    # Дальше читать нельзя Жуку А С
    # Остальным можно
    def start_calc(self):
        self.start_x_getter()
        self.start_y_getter()
        try:
            self.x_start = float(self.x_start)
            self.y_start = float(self.y_start)
            step_start = float(self.start_step_getter())
            iter = float(self.iter_getter())
            delay = float(self.delay_getter())

            self.window.updatePoint(self.x_start, self.y_start,
                                    self.function.get_function_point(self.x_start, self.y_start), color='red',
                                    delay=delay)

            arrowHeight = self.window.graph.axes.get_zlim()[1] / 10
            self.window.graph.draw_arrow(self.x_start, self.y_start,
                                         self.function.get_function_point(self.x_start, self.y_start) + arrowHeight,
                                         0, 0, -arrowHeight)

            self.window.textOutput.clear()
            grad = Gradient(self.function, self.x_start, self.y_start, iterations=iter, stepSize=step_start)
            for i, el in enumerate(grad.gradient_descent()):
                if i != 0:
                    self.window.updatePoint(*el[:3], delay=delay)
                text = f'{i}:  (x, y, function) = ({round(el[0], 5)}, {round(el[1], 5)}, {round(el[2], 5)})'
                self.window.updateText(text, delay=delay)
                point = el[:3]

            self.window.updatePoint(*point, color='green', delay=delay)
            self.window.graph.draw_arrow(point[0], point[1], point[2] + arrowHeight, 0, 0, -arrowHeight, color='green')

        except TypeError or ValueError as ex:
            print(ex)

# class Worker(QRunnable):
#     def __init__(self, fn, *args, **kwargs):
#         super(Worker, self).__init__()
#
#         # Store constructor arguments (re-used for processing)
#         self.fn = fn
#         self.args = args
#         self.kwargs = kwargs
#         self.signal = pyqtSignal(float,float,float,str,str)
#
#     @pyqtSlot()
#     def run(self):
#         result = self.fn(*self.args, **self.kwargs)
#         self.signals.result.emit(result)
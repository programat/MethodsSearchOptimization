import numpy as np
from abc import ABC, abstractmethod


class Functions(ABC):
    def __init__(self, x_interval_str, y_interval_str):
        try:
            self.x_interval = list(map(float, x_interval_str.replace(')', '', 1).replace('(', '', 1).split(';')))
            self.y_interval = list(map(float, y_interval_str.replace(')', '', 1).replace('(', '', 1).split(';')))
        except Exception:
            self.x_interval = [-5,5]
            self.y_interval = [-5,5]
    @abstractmethod
    def get_function(self) -> tuple:
        pass

    @abstractmethod
    def get_function_point(self, x, y):
        pass

    @abstractmethod
    def get_derivative(self, x, y):
        pass


class MatiasFunction(Functions):
    def get_function(self):
        x = np.arange(self.x_interval[0], self.x_interval[1], 0.25)
        y = np.arange(self.y_interval[0], self.y_interval[1], 0.25)
        x, y = np.meshgrid(x, y)
        z = .26 * (x ** 2 + y ** 2) - .48 * x * y
        return x, y, z

    def get_derivative(self, x, y):
        return .52 * x - .48 * y, .52 * y - .48 * x

    def get_function_point(self, x, y):
        return .26 * (x ** 2 + y ** 2) - .48 * x * y


class SphereFunction(Functions):
    def get_function(self):
        x = np.arange(self.x_interval[0], self.x_interval[1], 0.25)
        y = np.arange(self.y_interval[0], self.y_interval[1], 0.25)
        x, y = np.meshgrid(x, y)
        z = np.array(x**2+y**2)
        return x, y, z

    def get_derivative(self, x, y):
        return 2*x, 2*y

    def get_function_point(self, x, y):
        return x**2+y**2

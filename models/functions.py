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


class MatiasFunction(Functions):
    def get_function(self):
        x = np.arange(self.x_interval[0], self.x_interval[1], 0.25)
        y = np.arange(self.y_interval[0], self.y_interval[1], 0.25)
        x, y = np.meshgrid(x, y)
        z = .26 * (x ** 2 + y ** 2) - .48 * x * y
        return x, y, z

class SphereFunction(Functions):
    def get_function(self):
        x = np.arange(self.x_interval[0], self.x_interval[1], 0.25)
        y = np.arange(self.y_interval[0], self.y_interval[1], 0.25)
        x, y = np.meshgrid(x, y)
        z = np.array(x**2+y**2)
        return x, y, z

import math

import numpy as np
from abc import ABC, abstractmethod


class Functions(ABC):
    def __init__(self, x_interval_str='(-5;5)', y_interval_str='(-5;5)'):
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

class RastriginFunction(Functions):
    def get_function(self) -> tuple:
        x = np.arange(self.x_interval[0], self.x_interval[1], 0.25)
        y = np.arange(self.y_interval[0], self.y_interval[1], 0.25)
        x, y = np.meshgrid(x, y)
        z = 10*2 + np.array(x ** 2 - 10 * np.cos(2*math.pi*x)) + np.array(y ** 2 - 10 * np.cos(2*math.pi*y))
        return x, y, z

    def get_derivative(self, x, y):
        return 0

    def get_function_point(self, x, y):
        return 10*2 + (x ** 2 - 10 * np.cos(2*math.pi*x)) + (y ** 2 - 10 * np.cos(2*math.pi*y))


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

class AckleyFunction(Functions):
    def get_function(self):
        x = np.arange(self.x_interval[0], self.x_interval[1], 0.25)
        y = np.arange(self.y_interval[0], self.y_interval[1], 0.25)
        x, y = np.meshgrid(x, y)
        a = 20
        b = 0.2
        c = 2 * np.pi
        term1 = -a * np.exp(-b * np.sqrt(0.5 * (x**2 + y**2)))
        term2 = -np.exp(0.5 * (np.cos(c * x) + np.cos(c * y)))
        z = a + np.exp(1) + term1 + term2
        return x, y, z

    def get_derivative(self, x, y):
        a = 20
        b = 0.2
        c = 2 * np.pi
        e = np.exp(1)
        sqrt_term = np.sqrt(x**2 + y**2)
        cos_term_x = np.cos(c * x)
        cos_term_y = np.cos(c * y)

        dz_dx = -a * np.exp(-0.141421 * sqrt_term) - np.exp(.5*(cos_term_x + cos_term_y)) + 20 + np.exp(1)
        dz_dy = -a * np.exp(-0.141421 * sqrt_term) - np.exp(.5*(cos_term_x + cos_term_y)) + 20 + np.exp(1)

        return dz_dx, dz_dy

    def get_function_point(self, x, y):
        a = 20
        b = 0.2
        c = 2 * np.pi
        term1 = -a * np.exp(-b * np.sqrt(0.5 * (x**2 + y**2)))
        term2 = -np.exp(0.5 * (np.cos(c * x) + np.cos(c * y)))
        return a + np.exp(1) + term1 + term2

class CamelThreeHumpFunction(Functions):
    def get_function(self):
        x = np.arange(self.x_interval[0], self.x_interval[1], 0.25)
        y = np.arange(self.y_interval[0], self.y_interval[1], 0.25)
        x, y = np.meshgrid(x, y)
        z = 2*x**2 - 1.05*x**4 + x**6/6 + x*y + y**2
        return x, y, z

    def get_derivative(self, x, y):
        df_dx = x**5 - 4.2 * x**3 + 4 * x + y
        df_dy = x + 2 * y
        return df_dx, df_dy

    def get_function_point(self, x, y):
        return 2*x**2 - 1.05*x**4 + x**6/6 + x*y + y**2


class FunctionLab2(Functions):
    def get_function(self):
        x = np.arange(self.x_interval[0], self.x_interval[1], 0.25)
        y = np.arange(self.y_interval[0], self.y_interval[1], 0.25)
        x, y = np.meshgrid(x, y)
        z = 2 * x ** 2 + 3 * y ** 2 + 4 * x * y - 6 * x - 3 * y
        return x, y, z

    def get_derivative(self, x, y):
        pass

    def get_function_point(self, x, y):
        return 2 * x ** 2 + 3 * y ** 2 + 4 * x * y - 6 * x - 3 * y


class RosenbrockFunction(Functions):
    def get_function(self):
        x = np.arange(self.x_interval[0], self.x_interval[1], 0.25)
        y = np.arange(self.y_interval[0], self.y_interval[1], 0.25)
        x, y = np.meshgrid(x, y)
        z = (1 - x)**2 + 100 * (y - x**2)**2
        return x, y, z

    def get_function_point(self, x, y):
        return (1 - x)**2 + 100 * (y - x**2)**2

    def get_derivative(self, x, y):
        dx = -2 * (1 - x) - 400 * x * (y - x**2)
        dy = 200 * (y - x**2)
        return dx, dy
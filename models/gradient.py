from random import random
import numpy as np
from models.functions import MatiasFunction, SphereFunction


class Gradient:
    def __init__(self, function_to_calc, x, y, iterations, stepSize=random() * 2):
        self.x = x
        self.y = y
        self.gradient_value = None
        self.function = function_to_calc
        self.eps1 = .0001
        self.eps2 = .0001
        self.iterationCount = iterations
        self.stepSize = stepSize
        # print("step is ", self.stepSize)

    @property
    def iterations(self):
        return self.iterationCount

    @iterations.setter
    def iterations(self, numberOfIterations):
        self.iterationCount = numberOfIterations

    @property
    def step(self):
        return self.stepSize

    @step.setter
    def step(self, value):
        self.stepSize = value

    def gradient(self):
        self.gradient_value = self.function.get_derivative(self.x, self.y)

    def gradient_descent(self):
        def next_point() -> tuple:
            self.gradient()
            return self.x - self.step * self.gradient_value[0], self.y - self.step * self.gradient_value[1]

        yield self.x, self.y, self.function.get_function_point(self.x, self.y), 0

        self.gradient()

        k = 0
        while k < self.iterations:
            if np.linalg.norm(self.gradient_value) < self.eps1: break
            if k >= self.iterations: break

            x1, y1 = next_point()  # 7
            func1 = self.function.get_function_point(x1, y1)
            func0 = self.function.get_function_point(self.x, self.y)

            while not func1 < func0:
                self.stepSize /= 2
                x1, y1 = next_point()
                func1 = self.function.get_function_point(x1, y1)
                func0 = self.function.get_function_point(self.x, self.y)

            if np.linalg.norm(np.array([y1, x1]) - np.array([self.y, self.x])) < self.eps2 and abs(
                    func1 - func0) < self.eps2:  # 9
                break
            else:
                k += 1
                self.x, self.y = x1, y1
                yield self.x, self.y, func1, k


if __name__ == '__main__':
    grad = Gradient(MatiasFunction(0, 0), 2, 2, 100)
    ans = [[], [], []]
    for el in grad.gradient_descent():
        ans[0].append(el[0])
        ans[1].append(el[1])
        ans[2].append(el[2])

    print(f'{ans[0][-1]}\n'
          f'{ans[1][-1]}\n'
          f'{ans[2][-1]}')

import numpy as np


def make_data_himmelblau(p_X, p_Y):
    x = np.linspace(-p_X, p_X, 100)
    y = np.linspace(-p_Y, p_Y, 100)

    x_grid, y_grid = np.meshgrid(x, y)

    z = himmelblau(np.array([x_grid, y_grid]))
    return x_grid, y_grid, z


def himmelblau(x):
    return np.sum(2 * x[:-1] ** 2 + 3 * x[1:] ** 2 + 4 * x[:-1] * x[1:] - 6 * x[:-1] - 3 * x[1:], axis=0)


def himmelblau_2(x, y):
    return 2 * x * x + 3 * y * y + 4 * x * y - 6 * x - 3 * y


def make_data_rosenbrock(p_X, p_Y):
    x = np.linspace(-p_X, p_X, 100)
    y = np.linspace(-p_Y, p_Y, 100)

    x_grid, y_grid = np.meshgrid(x, y)

    z = rosenbrock(np.array([x_grid, y_grid]))
    return x_grid, y_grid, z


def rosenbrock(x):
    return np.sum(100.0 * (x[1:] - x[:-1] ** 2.0) ** 2.0 + (1 - x[:-1]) ** 2.0, axis=0)


def rosenbrock_2(x, y):
    return (1.0 - x) ** 2 + 100.0 * (y - x * x) ** 2


def make_data_rastrigin(p_X, p_Y):
    x = np.linspace(-p_X, p_X, 100)
    y = np.linspace(-p_Y, p_Y, 100)

    x_grid, y_grid = np.meshgrid(x, y)

    z = rastrigin(np.array([x_grid, y_grid]))
    return x_grid, y_grid, z


def rastrigin(x):
    return np.sum(x[1:] ** 2 - 10 * np.cos(2 * np.pi * x[1:]) + x[:-1] ** 2 - 10 * np.cos(2 * np.pi * x[:-1]), axis=0)


def rastrigin_2(x, y):
    return x ** 2 - 10 * np.cos(2 * np.pi * x) + y ** 2 - 10 * np.cos(2 * np.pi * y)


def hypersphere_2(x, y):
    return x ** 2 + y ** 2
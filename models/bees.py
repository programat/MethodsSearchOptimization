import random
from operator import itemgetter

import numpy as np


class Bees:
    """
    Класс для реализации алгоритма пчелиного роя.

    Args:
        func (callable): Целевая функция для оптимизации.
        scouts (int): Количество разведчиков.
        elite (int): Количество элитных участков.
        perspect (int): Количество перспективных участков.
        bees_to_leet (int): Количество рабочих пчел для каждого элитного участка.
        bees_to_persp (int): Количество рабочих пчел для каждого перспективного участка.
        radius (float): Радиус поиска.
        position_x (float): Максимальное значение координаты x.
        position_y (float): Максимальное значение координаты y.
        neighbourhood (str): Тип соседства для поиска рабочими пчелами ("square" или "circle").
    """

    def __init__(self, func, scouts, elite, perspect, bees_to_leet,
                 bees_to_persp, radius, position_x, position_y, neighbourhood="square"):
        self.func = func
        self.pos_x = float(position_x)
        self.pos_y = float(position_y)
        self.neighbourhood = neighbourhood

        # Инициализация разведчиков
        self.scouts = [[random.uniform(-self.pos_x, self.pos_x),
                        random.uniform(-self.pos_y, self.pos_y),
                        float(0.0)] for _ in range(scouts)]

        for scout in self.scouts:
            scout[2] = self.func(scout[0], scout[1])

        # Инициализация рабочих пчел
        self.n_workers = elite * bees_to_leet + perspect * bees_to_persp
        self.e = elite
        self.p = perspect
        self.b_leet = bees_to_leet
        self.b_persp = bees_to_persp

        max_b = max(self.scouts, key=itemgetter(2))
        self.workers = [[self.pos_x, self.pos_y, max_b[2]] for _ in range(self.n_workers)]

        self.bees = list()
        self.selected = list()
        self.rad = radius

    def send_scouts(self):
        """Перемещает разведчиков в случайные позиции и пересчитывает значение целевой функции."""
        for scout in self.scouts:
            scout[0] = random.uniform(-self.pos_x, self.pos_x)
            scout[1] = random.uniform(-self.pos_y, self.pos_y)
            scout[2] = self.func(scout[0], scout[1])

    def research_reports(self):
        """Сортирует всех пчел и выбирает лучшие участки."""
        self.bees = self.scouts + self.workers
        self.bees = sorted(self.bees, key=itemgetter(2), reverse=False)
        self.selected = self.bees[:self.e + self.p]

    def get_best(self):
        """Возвращает пчелу с лучшим значением целевой функции."""
        return self.bees[0]

    def send_workers(self, bee_part, sector, radius):
        """Перемещает рабочих пчел в окрестности выбранного участка."""
        for worker in bee_part:
            if self.neighbourhood == "square":
                worker[0] = random.uniform(sector[0] - radius, sector[0] + radius)
                worker[1] = random.uniform(sector[1] - radius, sector[1] + radius)
            elif self.neighbourhood == "circle":
                # Генерация случайной точки в круге
                theta = random.uniform(0, 2 * np.pi)
                r = radius * np.sqrt(random.uniform(0, 1))
                worker[0] = sector[0] + r * np.cos(theta)
                worker[1] = sector[1] + r * np.sin(theta)
            worker[2] = self.func(worker[0], worker[1])

    def selected_search(self, param):
        """Отправляет рабочих пчел на выбранные участки с уменьшением радиуса поиска."""
        for i in range(self.e):
            self.send_workers(
                self.workers[i * self.b_leet: i * self.b_leet + self.b_leet],
                self.selected[i],
                self.rad * param,
            )

        for i in range(self.p):
            self.send_workers(
                self.workers[
                self.e * self.b_leet + i * self.b_persp: self.e * self.b_leet + i * self.b_persp + self.b_persp
                ],
                self.selected[self.e + i],
                self.rad * param,
            )

    def run(self, max_iter):
        """
        Запускает алгоритм пчелиного роя на заданное количество итераций.

        Args:
            max_iter (int): Количество итераций.

        Yields:
            tuple: Кортеж, содержащий список всех пчел, список выбранных участков и лучшую пчелу.
        """
        for i in range(max_iter):
            self.send_scouts()
            self.research_reports()
            self.selected_search(1 / (i + 1))
            best_bee = self.get_best()
            yield self.bees, self.selected, best_bee

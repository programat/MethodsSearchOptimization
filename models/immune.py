import random
from operator import itemgetter
from functions import *  # Assuming you have a file 'functions.py' with your objective functions


class Immunity:
    """
    Класс для реализации иммунного алгоритма с клональной селекцией.

    Args:
        func (callable): Целевая функция для оптимизации.
        agents (int): Количество агентов (потенциальных решений) в популяции.
        clons (int): Количество клонов, создаваемых для каждого выбранного агента.
        best (int): Количество лучших агентов, выбираемых для клонирования.
        best_clon_numb (int): Количество лучших клонов, выбираемых для добавления в популяцию.
        position_x (float): Максимальное значение координаты x для инициализации агентов.
        position_y (float): Максимальное значение координаты y для инициализации агентов.
        mutation_rate (float): Вероятность мутации клона (по умолчанию 0.2).
    """

    def __init__(self, func, agents, clons, best, best_clon_numb, position_x, position_y, mutation_rate=0.2):
        self.func = func
        self.pos_x = float(position_x)
        self.pos_y = float(position_y)
        self.agents_numb = agents
        self.agents = self.initialize_population()  # Инициализируем популяцию агентов
        self.best = best
        self.best_clon_numb = best_clon_numb
        self.clon_numb = clons
        self.mutation_rate = mutation_rate

    def initialize_population(self):
        """
        Создает начальную популяцию агентов со случайными позициями.
        """
        return [[random.uniform(-self.pos_x, self.pos_x),
                 random.uniform(-self.pos_y, self.pos_y),
                 self.func(random.uniform(-self.pos_x, self.pos_x), random.uniform(-self.pos_y, self.pos_y))]
                for _ in range(self.agents_numb)]

    def immune_step(self, coef):
        """
        Выполняет один шаг иммунного алгоритма: селекция, клонирование, мутация, оценка и замена.

        Args:
            coef (float): Коэффициент, влияющий на степень мутации (обычно уменьшается с каждой итерацией).
        """
        # Selection (Best Individuals) - Выбираем лучших агентов для клонирования
        best_pop = sorted(self.agents, key=itemgetter(2), reverse=False)[:self.best]

        # Cloning - Клонируем выбранных агентов
        new_pop = []
        for pop in best_pop:
            clones = [pop.copy() for _ in range(self.clon_numb)]
            new_pop.extend(clones)

        # Mutation with adaptive rate - Мутируем клоны с адаптивной вероятностью
        for npop in new_pop:
            if random.random() < self.mutation_rate:
                # Mutation based on fitness - Степень мутации зависит от приспособленности
                npop[0] = npop[0] + coef * random.uniform(-0.5, 0.5) * (1 - npop[2] / self.agents[-1][2])
                npop[1] = npop[1] + coef * random.uniform(-0.5, 0.5) * (1 - npop[2] / self.agents[-1][2])
            npop[2] = self.func(npop[0], npop[1])  # Пересчитываем приспособленность после мутации

        # Evaluation and Selection (Best Clones) - Выбираем лучших клонов
        new_pop = sorted(new_pop, key=itemgetter(2), reverse=False)[:self.best_clon_numb]

        # Replacement - Заменяем худших агентов лучшими клонами
        self.agents += new_pop
        self.agents = sorted(self.agents, key=itemgetter(2), reverse=False)[:self.agents_numb]

    def get_best(self):
        """
        Возвращает агента с наилучшей приспособленностью (наименьшим значением целевой функции).
        """
        return self.agents[0]

    def run(self, max_iter):
        """
        Запускает иммунный алгоритм на заданное количество итераций и
        возвращает генератор для визуализации результатов.

        Args:
            max_iter (int): Количество итераций алгоритма.

        Yields:
            tuple: Кортеж, содержащий:
                *   list: Список всех агентов с их позициями и приспособленностью.
                *   list: Лучший агент на текущей итерации.
        """
        for i in range(max_iter):
            self.immune_step(1 / (i + 1))
            best_agent = self.get_best()
            all_points = [[agent[0], agent[1], agent[2]] for agent in self.agents]
            yield all_points, best_agent

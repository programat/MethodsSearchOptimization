from models.functions import FunctionLab2

class Simplex:
    def __init__(self, debug=False):
        self.function = FunctionLab2()
        self.func = [-8, -10, -2, -5, 1, 1, 9]
        self.terms = [
            [6, 4, 4, 1, 2, -1, 0, '<='],
            [3, 4, 6, 1, 3, 0, -1, '<='],
            [1, 1, 1, 0, 0, 0, 0, '<='],
            [4, 2, 3, 0, 0, 0, 0, '<=']
        ]
        self.n = 0
        self.m = 0
        self.table = []
        self.basis = []
        self.result = []
        self.mainCol = -1
        self.mainRow = -1

        self.debug = debug

    def calcOriginalFunc(self):
        return self.function.get_function_point(self.result[0], self.result[1])

    def startUp(self):
        # Сформировали первую матрицу
        self.m = len(self.terms)
        self.n = len(self.terms[0]) - 1
        self.table = [[0] * (self.n + self.m) for _ in range(self.m + 1)]

        for i in range(self.m):
            for j in range(self.n + self.m):
                if j < self.n:
                    self.table[i][j] = self.terms[i][j]
                else:
                    self.table[i][j] = 0

            if (self.n + i) < self.n + self.m:
                if self.terms[i][-1] == '<=':
                    self.table[i][self.n + i] = 1
                else:
                    self.table[i][self.n + i] = -1
                self.basis.append((self.n + i))
        self.table[self.m][0] = self.func[-1]
        for i in range(1, self.n):
            self.table[self.m][i] = -1 * self.func[i - 1]
        self.n = self.n + self.m
        self.m = self.m + 1

        self.result = [0] * (len(self.terms[-1]) - 2)

        for x, y, func in self.Calculate():
            yield x, y, func

        if self.debug: [print(i) for i in self.table]
        if self.debug: print('Значения переменных:', self.result)
        if self.debug: print('Мин значение функции:', sum([self.func[i] * self.result[i] for i in range(len(self.result))]))
        if self.debug: print(self.result[0], self.result[1])
        # print('Минимум оригинала:',
        # yield self.result[0], self.result[1],self.calcOriginalFunc()

    def Calculate(self):
        while (not self.isItEnd()):
            self.findMainCol()
            self.fineMainRow()
            self.basis[self.mainRow] = self.mainCol

            if self.debug: print('Базис:', self.basis)
            if self.debug: print('Ведущий стобец', self.mainCol)
            if self.debug: print('Ведущая строка', self.mainRow)

            new_table = [[0] * self.n for i in range(self.m)]
            for j in range(self.n):
                new_table[self.mainRow][j] = self.table[self.mainRow][j] / self.table[self.mainRow][self.mainCol]
            for i in range(self.m):
                if i == self.mainRow:
                    continue
                for j in range(self.n):
                    new_table[i][j] = self.table[i][j] - self.table[i][self.mainCol] * new_table[self.mainRow][j]
            self.table = new_table
            if self.debug:
                print('Таблица:')
                for t in self.table:
                    print(t)
                print('Базис:', self.basis)
                print('Ведущий стобец', self.mainCol)
                print('Ведущая строка', self.mainRow)
            for i in range(len(self.result)):
                try:
                    k = self.basis.index(i + 1)
                except Exception:
                    k = -1

                if k != -1:
                    self.result[i] = self.table[k][0]
                else:
                    self.result[i] = 0
            yield self.result[0], self.result[1], self.calcOriginalFunc()

    def findMainCol(self):
        self.mainCol = 1
        for j in range(2, self.n):
            if (self.table[self.m - 1][j]) > (self.table[self.m - 1][self.mainCol]):
                self.mainCol = j

    def fineMainRow(self):
        self.mainRow = 0
        for i in range(0, self.m - 1):
            if self.table[i][self.mainCol] > 0:
                self.mainRow = i
                break
        for i in range(self.mainRow + 1, self.m - 1):
            if (self.table[i][self.mainCol] > 0) and (
                    (self.table[i][0] / self.table[i][self.mainCol]) < (
                    self.table[self.mainRow][0] / self.table[self.mainRow][self.mainCol])):
                self.mainRow = i

    def isItEnd(self):
        flag = True
        for j in range(1, self.n):
            if self.table[self.m - 1][j] > 0:
                flag = False
                break
        return flag


if __name__ == '__main__':
    simplex = Simplex()
    for x1,x2,f in simplex.startUp():
        print(x1, x2, f, sep='\n', end='\n---\n')


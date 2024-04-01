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

    def start_calc(self):
        try:
            def Arrow3D(ax, x, y, z, dx, dy, dz, color='red', arrow_length_ratio=0.1, lw=2):
                ax.quiver(x, y, z, dx, dy, dz, color=color, arrow_length_ratio=arrow_length_ratio,
                          lw=lw)

            arrowHeight = self.window.graph.axes.get_zlim()[1] / 10

            self.window.textOutput.clear()
            simplex = Simplex()
            for i, el in enumerate(simplex.startUp()):
                if i == 0:
                    self.window.updatePoint(*el[:3], color='red')
                    Arrow3D(self.window.graph.axes, el[0], el[1],
                            el[2] + arrowHeight, 0, 0, -arrowHeight)
                else: self.window.updatePoint(*el[:3])
                self.window.textOutput.append(
                    f'{i}:  (x, y, function) = ({round(el[0], 5)}, {round(el[1], 5)}, {round(el[2], 5)})')
                point = el[:3]

            self.window.updatePoint(*point, color='green')


            # Arrow3D(self.window.graph.axes, self.x_start, self.y_start,
            #         -5 + arrowHeight, 0, 0, -arrowHeight)
            Arrow3D(self.window.graph.axes, point[0], point[1], point[2] + arrowHeight, 0, 0, -arrowHeight,
                    color='green')

        except TypeError or ValueError as ex:
            print(ex)

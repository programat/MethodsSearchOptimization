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

            self.window.updatePoint(self.x_start, self.y_start,
                                    self.function.get_function_point(self.x_start, self.y_start), color='red')

            self.window.textOutput.clear()
            grad = Gradient(self.function, self.x_start, self.y_start, iterations=iter, stepSize=step_start)
            for i, el in enumerate(grad.gradient_descent()):
                if i != 0: self.window.updatePoint(*el[:3])
                self.window.textOutput.append(
                    f'{i}:  (x, y, function) = ({round(el[0], 5)}, {round(el[1], 5)}, {round(el[2], 5)})')
                point = el[:3]
            self.window.updatePoint(*point, color='green')

            def Arrow3D(ax, x, y, z, dx, dy, dz, color='red', arrow_length_ratio=0.1, lw=2):
                ax.quiver(x, y, z, dx, dy, dz, color=color, arrow_length_ratio=arrow_length_ratio,
                          lw=lw)

            arrowHeight = self.window.graph.axes.get_zlim()[1]/10
            Arrow3D(self.window.graph.axes, self.x_start, self.y_start,
                    self.function.get_function_point(self.x_start, self.y_start) + arrowHeight, 0, 0, -arrowHeight)
            Arrow3D(self.window.graph.axes, point[0], point[1], point[2] + arrowHeight, 0, 0, -arrowHeight, color='green')

        except TypeError or ValueError as ex:
            print(ex)
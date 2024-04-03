from PyQt6 import QtWidgets
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class GraphWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.points = []
        self.arrows = []

        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.axes = self.fig.add_subplot(111, projection='3d',computed_zorder=False)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)

        self.axes.xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
        self.axes.yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
        self.axes.zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))


    def draw_graph(self, axes, z_mash, gridOn, axisOn, ticklabelsOn):
        # Clear the previous plot
        self.axes.clear()

        # Plot the new surface
        self.axes.set_box_aspect([1,1,z_mash])
        self.axes.plot_surface(axes[0], axes[1], axes[2], alpha=0.5, cmap='coolwarm')

        # True False
        self.axes.grid(gridOn)

        # True False
        self.axes.xaxis.line.set_visible(axisOn)
        self.axes.yaxis.line.set_visible(axisOn)
        self.axes.zaxis.line.set_visible(axisOn)

        if not ticklabelsOn:
            # Remove tick labels
            self.axes.xaxis.set_ticklabels([])
            self.axes.yaxis.set_ticklabels([])
            self.axes.zaxis.set_ticklabels([])

            # Remove ticks (small lines)
            self.axes.tick_params(axis='x', which='both', bottom=False, top=False)
            self.axes.tick_params(axis='y', which='both', left=False, right=False)
            self.axes.tick_params(axis='z', which='both', bottom=False, top=False)


        # Redraw the canvas
        self.canvas.draw()

    def draw_arrow(self, x, y, z, dx, dy, dz, color='red', arrow_length_ratio=0.1, lw=2):
        arrow = self.axes.quiver(x, y, z, dx, dy, dz, color=color, arrow_length_ratio=arrow_length_ratio, lw=lw)
        self.arrows.append(arrow)  # Сохраняем ссылку на стрелку
        self.canvas.draw()

    def remove_arrow(self, index):
        if 0 <= index < len(self.arrows):
            arrow = self.arrows.pop(index)  # Удаляем ссылку на стрелку из списка
            arrow.remove()  # Удаляем стрелку с графика
            self.canvas.draw()

    def clear_arrows(self):
        for arrow in self.arrows:
            arrow.remove()  # Удаляем все стрелки с графика
        self.arrows.clear()  # Очищаем список ссылок на стрелки
        self.canvas.draw()

    def draw_point(self, points, color='pink', marker='o'):
        for point in points:
            x, y, z = point
            self.points.append(self.axes.scatter(x, y, z, color=color, marker=marker, s=10, zorder=10))
        self.canvas.draw()

    def remove_point(self, index):
        if 0 <= index < len(self.points):
            point = self.points.pop(index)  # Удаляем ссылку на точку из списка
            point.remove()  # Удаляем точку с графика
            self.canvas.draw()

    def clear_points(self):
        for point in self.points:
            if isinstance(point, list):
                point.clear()
            else:
                point.remove()  # Удаляем все точки с графика
        self.points.clear()  # Очищаем список ссылок на точки
        self.canvas.draw()
        self.clear_arrows()


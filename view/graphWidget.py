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
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.axes = self.fig.add_subplot(111, projection='3d')

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)

        self.axes.xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
        self.axes.yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
        self.axes.zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))


    def draw_graph(self, axes, z_mash, gridOn, axisOn):
        # Clear the previous plot
        self.axes.clear()

        # Plot the new surface
        self.axes.set_box_aspect([1,1,z_mash])
        self.axes.plot_surface(axes[0], axes[1], axes[2], cmap='coolwarm')

        # True False
        self.axes.grid(gridOn)

        # True False
        self.axes.xaxis.line.set_visible(axisOn)
        self.axes.yaxis.line.set_visible(axisOn)
        self.axes.zaxis.line.set_visible(axisOn)

        self.axes.xaxis.set_ticklabels([])
        self.axes.yaxis.set_ticklabels([])
        self.axes.zaxis.set_ticklabels([])


        # Redraw the canvas
        self.canvas.draw()

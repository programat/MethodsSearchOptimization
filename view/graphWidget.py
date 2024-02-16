from PyQt6 import QtWidgets
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class GraphWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111, projection='3d')

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)

    def draw_graph(self, axes, z_mash, gridOn, axisOn):
        # Clear the previous plot
        self.axes.clear()

        # Plot the new surface
        self.axes.set_box_aspect([1,1,z_mash])
        self.axes.plot_surface(axes[0], axes[1], axes[2], cmap='coolwarm')
        self.axes.set_zlim([0,max(axes[2][0])])

        # True False
        self.axes.grid(gridOn)
        # on off
        self.axes.xaxis.line.set_visible(axisOn)
        self.axes.yaxis.line.set_visible(axisOn)
        self.axes.zaxis.line.set_visible(axisOn)

        self.axes.xaxis.set_ticklabels([])
        self.axes.yaxis.set_ticklabels([])
        self.axes.zaxis.set_ticklabels([])

        # Redraw the canvas
        self.canvas.draw()

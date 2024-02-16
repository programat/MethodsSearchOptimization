from PyQt6 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



class GraphWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111, projection='3d')

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)

    def draw_graph(self, axes, z_mash):
        # Clear the previous plot
        self.axes.clear()
        # Plot the new surface
        self.axes.plot_surface(axes[0], axes[1], axes[2], cmap='coolwarm')
        self.axes.set_zscale(z_mash)
        # Redraw the canvas
        self.canvas.draw()

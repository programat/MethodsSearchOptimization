import os
import sys
import time

from PyQt6.QtCore import QThreadPool, QRunnable, pyqtSignal, QThread
from PyQt6.QtGui import QFocusEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt6 import uic, QtWidgets

from view.graphWidget import GraphWidget
from controllers.mainWindowController import MainWindowController

from controllers.lab1Controller import Lab1Controller
from view.lab1View import Lab1View
from controllers.lab2Controller import Lab2Controller
from view.lab2View import Lab2View


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lab1_view = None
        self.lab1_controller = None
        self.graph = GraphWidget()
        self.controller = MainWindowController(self)

        self.point_thread = PointThread(self)
        self.point_thread.point_signal.connect(self.graph.draw_point)

        self.setupUi()


    def setupUi(self):
        uic.loadUi(os.path.join(os.path.dirname(__file__), '..//ui//app.ui'), self)
        layout = QtWidgets.QVBoxLayout(
            self.graphFrame)  # Assuming graphFrame is the name of a container widget in your UI
        layout.addWidget(self.graph)


        return self

    def create(self):
        self.lab1_controller = Lab1Controller(self)
        self.lab1_view = Lab1View(self, self.lab1_controller)
        self.lab2_controller = Lab2Controller(self)
        self.lab2_view = Lab2View(self, self.lab2_controller)

        self.controller.lab_selector()
        self.controller.functions_selector()

        self.grid.stateChanged.connect(lambda: self.controller.grid_change())
        self.axes.stateChanged.connect(lambda: self.controller.axes_change())
        self.functionSelector.currentTextChanged.connect(lambda: self.controller.functions_selector())
        self.x_interval.editingFinished.connect(lambda: self.controller.x_interval_changed())
        self.y_interval.editingFinished.connect(lambda: self.controller.y_interval_changed())
        self.z_scale.editingFinished.connect(lambda: self.controller.z_scale_changed())
        self.ticklabels.stateChanged.connect(lambda: self.controller.ticklabels_changed())

        self.tabWidget.currentChanged.connect(lambda: self.controller.lab_selector())

        self.clear_all.clicked.connect(lambda: self.controller.clear_all())

        return self

    def updateGraph(self, axes, z_scale, gridOn, axisOn, ticklabelsOn):
        self.graph.draw_graph(axes, z_scale, gridOn, axisOn, ticklabelsOn)

    def updatePoint(self, x, y, z, color='pink', marker='o', delay=0):
        self.point_thread.add_point(x, y, z, color, marker, delay)
        if not self.point_thread.isRunning():
            self.point_thread.start()

class PointThread(QThread):
    point_signal = pyqtSignal(float, float, float, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.points = []

    def add_point(self, x, y, z, color, marker, delay):
        self.points.append((x, y, z, color, marker, delay))

    def run(self):
        for point in self.points:
            x, y, z, color, marker, delay = point
            self.msleep(int(delay * 1000))
            self.point_signal.emit(x, y, z, color, marker)
        self.points.clear()

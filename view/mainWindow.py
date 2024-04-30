import os
import sys
import time

from PyQt6.QtCore import QThreadPool, QRunnable, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QFocusEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt6 import uic, QtWidgets

from view.graphWidget import GraphWidget
from controllers.mainWindowController import MainWindowController

from controllers.lab1Controller import Lab1Controller
from view.lab1View import Lab1View
from controllers.lab2Controller import Lab2Controller
from view.lab2View import Lab2View
from controllers.lab3Controller import Lab3Controller
from view.lab3View import Lab3View
from controllers.lab4Controller import Lab4Controller
from view.lab4View import Lab4View
from controllers.lab5Controller import Lab5Controller
from view.lab5View import Lab5View


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lab1_view = None
        self.lab1_controller = None
        self.graph = GraphWidget()
        self.controller = MainWindowController(self)

        self.setupUi()

        self.text_thread = TextThread(self)
        self.point_thread = PointThread(self)
        self.point_list_thread = PointListThread(self, self.graph)

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
        self.lab3_controller = Lab3Controller(self)
        self.lab3_view = Lab3View(self, self.lab3_controller)
        self.lab4_controller = Lab4Controller(self)
        self.lab4_view = Lab4View(self, self.lab4_controller)
        self.lab5_controller = Lab5Controller(self)
        self.lab5_view = Lab5View(self, self.lab5_controller)

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

        self.text_thread.text_signal.connect(self.textOutput.append)
        self.point_thread.point_signal.connect(self.graph.draw_point)
        self.point_list_thread.point_signal.connect(self.graph.draw_point)
        self.point_list_thread.clearPointsSignal.connect(self.graph.clear_points_dynamic)
        return self

    def updateGraph(self, axes, z_scale, gridOn, axisOn, ticklabelsOn):
        self.graph.draw_graph(axes, z_scale, gridOn, axisOn, ticklabelsOn)

    def updatePoint(self, points, color='pink', marker='o', delay=0):
        self.point_thread.add_points(points, color, marker, delay)
        if not self.point_thread.isRunning():
            self.point_thread.start()

    def updateListPoint(self, points, color='pink', marker='o', delay=0):
        self.point_list_thread.set_points(points, color, marker, delay)
        if not self.point_list_thread.isRunning():
            self.point_list_thread.start()

    def updateText(self, text, delay=0):
        self.text_thread.add_text(text, delay)
        if not self.text_thread.isRunning():
            self.text_thread.start()


class TextThread(QThread):
    text_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.texts = []

    def add_text(self, text, delay):
        self.texts.append((text, delay))

    def run(self):
        for text, delay in self.texts:
            self.msleep(int(delay * 1000))
            self.text_signal.emit(text)
        self.texts.clear()


class PointThread(QThread):
    point_signal = pyqtSignal(list, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.points = []

    def add_points(self, points, color, marker, delay):
        # self.points= []
        if isinstance(points, tuple):
            points = [points]
        # print(self.points)
        self.points.append((points, color, marker, delay))

    def run(self):
        for point_data in self.points:
            points, color, marker, delay = point_data
            self.msleep(int(delay * 1000))
            self.point_signal.emit(points, color, marker)
        # GraphWidget().clear_points()  # Очищаем список точек
        self.points.clear()


class PointListThread(QThread):
    point_signal = pyqtSignal(list, str, str)
    clearPointsSignal = pyqtSignal()  # Новый сигнал для очистки точек

    def __init__(self, parent, graph):
        super().__init__(parent)
        self.points = []
        self.painting = False
        self.graph = graph

    def add_points(self, points, color, marker, delay):
        self.points = []
        for el in points:
            self.points.append((el, color, marker, delay))
        # self.points=[points, color, marker, delay]
        # print(self.points)

    def set_points(self, points, color, marker, delay):
        # self.points.clear()
        self.add_points(points, color, marker, delay)

    def run(self):
        for i, el in enumerate(self.points):
            min_point = min(el[0], key=lambda x: x[2])
            self.point_signal.emit([min_point], 'red', 'o')
            self.point_signal.emit(el[0], el[1], el[2])
            self.msleep(int(el[3] * 1000))
            if i != len(self.points) - 1:
                self.clearPointsSignal.emit()


if __name__ == '__main__':
    el = ([[-0.8708019971500014, -2.835048193475976, 1294.7122343670067],
           [2.5610452515341384, -2.1829865304294636, 7644.587153709607],
           [-0.6797552716973527, -2.1114463604657185, 665.1187974953248]], 'pink', '.', 0.1)
    # print(min(el[0], key=lambda x: x[2]))

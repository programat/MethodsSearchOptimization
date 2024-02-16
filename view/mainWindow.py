import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic, QtWidgets
from view.graphWidget import GraphWidget
from controllers.mainWindowController import MainWindowController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.graph = GraphWidget()
        self.controller = MainWindowController(self)

    def create(self):
        uic.loadUi(os.path.join(os.path.dirname(__file__), '..//ui//app.ui'), self)
        self.controller.functions_selector()
        layout = QtWidgets.QVBoxLayout(
            self.graphFrame)  # Assuming graphFrame is the name of a container widget in your UI
        layout.addWidget(self.graph)

        self.grid.stateChanged.connect(lambda: self.controller.grid_change())
        self.axes.stateChanged.connect(lambda: self.controller.axes_change())
        self.functionSelector.currentTextChanged.connect(lambda: self.controller.functions_selector())

        return self

    def updateGraph(self, axes, z_scale, gridOn, axisOn):
        self.graph.draw_graph(axes, z_scale, gridOn, axisOn)

    # def closeEvent(self, QCloseEvent):
    #     # del self.controllers
    #     sys.exit()




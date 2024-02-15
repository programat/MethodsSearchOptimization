import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic, QtWidgets

import models.functions
from view.graphWidget import GraphWidget
from models import *


class MainWindowController:
    def __init__(self, window):
        self._window = window
        self.function = None

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, new):
        self._window = new
        
    def x_interval_getter(self):
        return self.window.x_interval.text()

    def y_interval_getter(self):
        return self.window.y_interval.text()

    def functions_selector(self):
        selected_function = self.window.functionSelector.currentText()
        if selected_function == 'Функция Матьяса':
            self.function = models.functions.MatiasFunction(x_interval_str=self.x_interval_getter(),
                                                            y_interval_str=self.y_interval_getter())
        elif selected_function == 'Функция сферы':
            self.function = models.functions.SphereFunction(x_interval_str=self.x_interval_getter(),
                                                            y_interval_str=self.y_interval_getter())

        self.window.updateGraph(self.function.get_function())

import os
import sys
import time

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import QTimer

import models.functions
from models.gradient import Gradient
from view.graphWidget import GraphWidget
from models import *


class MainWindowController:
    def __init__(self, window):
        self._window = window
        self.labClass = None
        self.function = None
        self.z_scale = None
        self.gridOn = True
        self.axisOn = True
        self.ticklabelsOn = True
        self.x_start = None
        self.y_start = None

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, new):
        self._window = new

    def x_interval_getter(self) -> str:
        return self.window.x_interval.text()

    def y_interval_getter(self) -> str:
        return self.window.y_interval.text()

    def z_scale_getter(self) -> float:
        self.z_scale = float(self.window.z_scale.text())
        return self.z_scale

    def grid_change(self):
        self.gridOn = self.window.grid.isChecked()
        self.window.updateGraph(self.function.get_function(), self.z_scale_getter(), self.gridOn, self.axisOn,
                                self.ticklabelsOn)
        return self.gridOn

    def axes_change(self):
        self.axisOn = self.window.axes.isChecked()
        self.window.updateGraph(self.function.get_function(), self.z_scale_getter(), self.gridOn, self.axisOn,
                                self.ticklabelsOn)
        return self.axisOn

    def ticklabels_changed(self):
        self.ticklabelsOn = self.window.ticklabels.isChecked()
        self.window.updateGraph(self.function.get_function(), self.z_scale_getter(), self.gridOn, self.axisOn,
                                self.ticklabelsOn)
        return self.ticklabelsOn

    def x_interval_changed(self):
        self.functions_selector()

    def y_interval_changed(self):
        self.functions_selector()

    def z_scale_changed(self):
        self.functions_selector()

    def functions_selector(self):
        selected_function = self.window.functionSelector.currentText()
        if selected_function == 'Функция Матьяса':
            self.function = models.functions.MatiasFunction(x_interval_str=self.x_interval_getter(),
                                                            y_interval_str=self.y_interval_getter())
        elif selected_function == 'Функция сферы':
            self.function = models.functions.SphereFunction(x_interval_str=self.x_interval_getter(),
                                                            y_interval_str=self.y_interval_getter())

        self.window.updateGraph(self.function.get_function(), self.z_scale_getter(), self.gridOn, self.axisOn,
                                self.ticklabelsOn)

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
            delay = float(self.delay_getter())

            grad = Gradient(self.function, self.x_start, self.y_start, iterations=iter, stepSize=step_start)
            for el in grad.gradient_descent():
                print(el)
                self.window.updatePoint(*el[:3])



        except TypeError or ValueError as ex:
            # QMessageBox.warning(self.window, "Warning", "Wrong Data")
            print(ex)

    # def point_plotting(self):

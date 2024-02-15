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

        layout = QtWidgets.QVBoxLayout(self.graphFrame)  # Assuming graphFrame is the name of a container widget in your UI
        layout.addWidget(self.graph)

        # Ивент открытия        # self.settings.clicked.connect(lambda : self.controllers.clicked_settings())
        # self.dir.clicked.connect(lambda :self.controllers.clicked_dir())
        # self.file.clicked.connect(lambda: self.controllers.clicked_file())
        # self.start.clicked.connect(lambda :self.controllers.clicked_start())
        # self.clearlogs.clicked.connect(lambda :self.controllers.clicked_clear())
        self.functionSelector.currentTextChanged.connect(lambda: self.controller.functions_selector())
        return self

    def updateGraph(self, axes):
        self.graph.draw_graph(axes)

    # def closeEvent(self, QCloseEvent):
    #     # del self.controllers
    #     sys.exit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow().create()
    w.show()
    sys.exit(app.exec())

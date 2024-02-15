import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Тут был контроллер
        # self.controller = main_window_controller.MainWindowController(self)

    def create(self):
        uic.loadUi(os.path.join(os.path.dirname(__file__), '..//ui//app.ui'), self)

        # Ивент открытия
        # self.settings.clicked.connect(lambda : self.controller.clicked_settings())
        # self.dir.clicked.connect(lambda :self.controller.clicked_dir())
        # self.file.clicked.connect(lambda: self.controller.clicked_file())
        # self.start.clicked.connect(lambda :self.controller.clicked_start())
        # self.clearlogs.clicked.connect(lambda :self.controller.clicked_clear())
        return self

    def show(self):
        super().show()
        return self

    # def closeEvent(self, QCloseEvent):
    #     # del self.controller
    #     sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow().create()
    w = w.show()
    sys.exit(app.exec())

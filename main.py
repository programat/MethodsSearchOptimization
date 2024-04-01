import sys

from PyQt6.QtWidgets import QApplication

from view.mainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.create()
    window.show()
    sys.exit(app.exec())
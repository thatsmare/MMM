import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QHBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class window(QMainWindow):
    def __init__(self): # automatically happens when class is called
        super().__init__() # activates QMainWindow - class in the ()
        self.setWindowTitle("Transfer Function I/O Illustration")
        self.setGeometry() #setGeometry(x, y, width, height) distance from left, from top



 #run
 if __name__ == "__test__":
    app = QApplication(sys.argv)
    windowapp = window()
    windowapp.show()
    sys.exit(app.exec_())       


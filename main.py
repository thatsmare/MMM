import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit,
    QPushButton, QLabel, QHBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transfer Function I/O Illustration")
        self.setGeometry(100, 100, 1200, 800)

        self.start_menu()

    def start_menu(self):
        layout = QHBoxLayout()
        start_b = QPushButton("Start")
        layout.addWidget(start_b)
        start_b.clicked.connect(self.central_part)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def central_part(self):
        self.main_display = QVBoxLayout()

        controls_view = QHBoxLayout()
        menu_b = QPushButton("Menu")
        controls_view.addWidget(menu_b)
        menu_b.clicked.connect(self.menu_display)

        self.main_display.addLayout(controls_view)

        central_widget = QWidget()
        central_widget.setLayout(self.main_display)
        self.setCentralWidget(central_widget)

    def menu_display(self):

        menu_view = QHBoxLayout()
        self.nominator_input = QLineEdit("nominator")
        self.denominator_input = QLineEdit("denominator")
        set_b = QPushButton("Set parameters")
        back_b = QPushButton("Close")

        back_b.clicked.connect(self.central_part)

        menu_view.addWidget(QLabel("Nominator of G :"))
        menu_view.addWidget(self.nominator_input)
        menu_view.addWidget(QLabel("Denominator of G :"))
        menu_view.addWidget(self.denominator_input)
        menu_view.addWidget(set_b)
        menu_view.addWidget(back_b)


        menu_widget = QWidget()
        menu_widget.setLayout(menu_view)
        self.setCentralWidget(menu_widget)


#run
if __name__ == "__main__":
    app = QApplication(sys.argv)
    windowapp = Window()
    windowapp.show()
    sys.exit(app.exec_())

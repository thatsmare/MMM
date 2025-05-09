import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit,
    QPushButton, QLabel, QHBoxLayout, QRadioButton
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transfer Function I/O Illustration")
        self.setGeometry(100, 100, 1200, 800)

        self.start_menu()

    def start_menu(self):
        layout = QVBoxLayout()

        title = QLabel("<h1>Projekt 10 - implementacja symulatora układu opisanego za pomocą transmitancji</h1>")
        title.setAlignment(Qt.AlignCenter)

        description = QLabel("Symulator umożliwia uzyskanie odpowiedzi czasowych układu na pobudzenie sygnałem" \
        " prostokątnym o skończonym czasie trwania, trójkątnym i sinusoidalnym o zadanych parametrach. Możliwa jest zmiana wszystkich" \
        " współczynników licznika i mianownika transmitancji. Program wykreśla charakterystyki częstotliwościowe Bodego oraz sygnał wejściowy" \
        " i wyjściowy, na podstawie czego określa stabliność układu.")
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)

        start_b = QPushButton("Menu")
        start_b.clicked.connect(self.menu_display)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(start_b)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def menu_display(self):

        menu_view = QVBoxLayout()
        self.nominator_input = QLineEdit("nominator")
        self.denominator_input = QLineEdit("denominator")
        set_b = QPushButton("Set parameters")
        back_b = QPushButton("Close")

        back_b.clicked.connect(self.start_menu)

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

"""
class transfer_function:
    def poles():
    #przekształca podane współczynniki bn na postać mianownika i liczy miejsca zerowe
        
    def zeros():
    #przekształca podane współczynniki an na postać licznika i liczy miejsca zerowe

    def transfer_show():
    #wyświetlenie transmitancji w oknie


class input signal:
    def sin():
    #ustawienie parametrów sinusoidy

    def square():
    
    def triangle():
    
    def input_plot():
    #rysowanie sygnały wejściowego
    

class output_signal:
    def output_s():
    #wyjście w dziedzinie operatorowej znając G(s) i U(s)

    def differentiation():
    #różniczkowanie metodą numeryczną do uzyskania odpowiedzi w dziedzinie czasu

    def output_plot():
    #rysowanie sygnału wyjściowego

    
class bode:
    def amplitude():
    #algorytm na funkcje i rysowanie
    
    def phase():
    #algorytm na funkcje i rysowanie

"""
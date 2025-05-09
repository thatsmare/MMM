import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit,
    QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QRadioButton, QGroupBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

"""
class transfer_function:
    def poles():
    #przekształca podane współczynniki bn na postać mianownika i liczy miejsca zerowe
        
    def zeros():
    #przekształca podane współczynniki an na postać licznika i liczy miejsca zerowe

    def transfer_show():
    #wyświetlenie transmitancji w oknie
    """

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transfer Function I/O Illustration")
        self.setGeometry(100, 100, 1200, 800)

        self.start_menu()

    def update_coefficient(self, line_edit, attr_name):
        try:
            value = float(line_edit.text())
        except ValueError:
            value = 0  
        setattr(self, attr_name, value)

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

        #WARTOŚCI POCZĄTKOWE ALE FINALNIE NA PEWNO NIE W TYM MIEJSCU
        self.b4 = 0
        self.b3 = 0
        self.b2 = 0
        self.b1 = 0
        self.b0 = 0
        self.a4 = 0
        self.a3 = 0
        self.a2 = 0
        self.a1 = 0
        self.a0 = 0

    def menu_display(self):
        menu_view = QVBoxLayout()
        self.nominator_a3_input = QLineEdit(str(self.a3))
        self.nominator_a2_input = QLineEdit(str(self.a2))
        self.nominator_a1_input = QLineEdit(str(self.a1))
        self.nominator_a0_input = QLineEdit(str(self.a0))
        self.denominator_b4_input = QLineEdit(str(self.b4))
        self.denominator_b3_input = QLineEdit(str(self.b3))
        self.denominator_b2_input = QLineEdit(str(self.b2))
        self.denominator_b1_input = QLineEdit(str(self.b1))
        self.denominator_b0_input = QLineEdit(str(self.b0))
        set_b = QPushButton("Simulate")
        back_b = QPushButton("Back to start")

        set_b.clicked.connect(self.simulation)
        back_b.clicked.connect(self.start_menu)

        menu_view.addWidget(QLabel("<h3>Coefficients of transfer function</h3>"))
        menu_view.addWidget(QLabel("Nominator of G :"))
        self.nominator_a3_input.setFixedWidth(80)
        self.nominator_a3_input.editingFinished.connect(lambda: self.update_coefficient(self.nominator_a3_input, "a3"))
        a3_layout = QHBoxLayout()
        a3_layout.setAlignment(Qt.AlignLeft)
        a3_layout.addWidget(QLabel("a3:"))
        a3_layout.addWidget(self.nominator_a3_input)
        a3_layout.addStretch()
        menu_view.addLayout(a3_layout)

        self.nominator_a2_input.setFixedWidth(80)
        self.nominator_a2_input.editingFinished.connect(lambda: self.update_coefficient(self.nominator_a2_input, "a2"))
        a2_layout = QHBoxLayout()
        a2_layout.setAlignment(Qt.AlignLeft)
        a2_layout.addWidget(QLabel("a2:"))
        a2_layout.addWidget(self.nominator_a2_input)
        a2_layout.addStretch()
        menu_view.addLayout(a2_layout)

        self.nominator_a1_input.setFixedWidth(80)
        self.nominator_a1_input.editingFinished.connect(lambda: self.update_coefficient(self.nominator_a1_input, "a1"))
        a1_layout = QHBoxLayout()
        a1_layout.setAlignment(Qt.AlignLeft)
        a1_layout.addWidget(QLabel("a1:"))
        a1_layout.addWidget(self.nominator_a1_input)
        a1_layout.addStretch()
        menu_view.addLayout(a1_layout)

        self.nominator_a0_input.setFixedWidth(80)
        self.nominator_a0_input.editingFinished.connect(lambda: self.update_coefficient(self.nominator_a0_input, "a0"))
        a0_layout = QHBoxLayout()
        a0_layout.setAlignment(Qt.AlignLeft)
        a0_layout.addWidget(QLabel("a0:"))
        a0_layout.addWidget(self.nominator_a0_input)
        a0_layout.addStretch()
        menu_view.addLayout(a0_layout)

        menu_view.addWidget(QLabel("Denominator of G :"))
        self.denominator_b4_input.setFixedWidth(80)
        self.denominator_b4_input.editingFinished.connect(lambda: self.update_coefficient(self.denominator_b4_input, "b4"))
        b4_layout = QHBoxLayout()
        b4_layout.setAlignment(Qt.AlignLeft)
        b4_layout.addWidget(QLabel("b4:"))
        b4_layout.addWidget(self.denominator_b4_input)
        b4_layout.addStretch()
        menu_view.addLayout(b4_layout)

        self.denominator_b3_input.setFixedWidth(80)
        self.denominator_b3_input.editingFinished.connect(lambda: self.update_coefficient(self.denominator_b3_input, "b3"))
        b3_layout = QHBoxLayout()
        b3_layout.setAlignment(Qt.AlignLeft)
        b3_layout.addWidget(QLabel("b3:"))
        b3_layout.addWidget(self.denominator_b3_input)
        b3_layout.addStretch()
        menu_view.addLayout(b3_layout)

        self.denominator_b2_input.setFixedWidth(80)
        self.denominator_b2_input.editingFinished.connect(lambda: self.update_coefficient(self.denominator_b2_input, "b2"))
        b2_layout = QHBoxLayout()
        b2_layout.setAlignment(Qt.AlignLeft)
        b2_layout.addWidget(QLabel("b2:"))
        b2_layout.addWidget(self.denominator_b2_input)
        b2_layout.addStretch()
        menu_view.addLayout(b2_layout)

        self.denominator_b1_input.setFixedWidth(80)
        self.denominator_b1_input.editingFinished.connect(lambda: self.update_coefficient(self.denominator_b1_input, "b1"))
        b1_layout = QHBoxLayout()
        b1_layout.setAlignment(Qt.AlignLeft)
        b1_layout.addWidget(QLabel("b1:"))
        b1_layout.addWidget(self.denominator_b1_input)
        b1_layout.addStretch()
        menu_view.addLayout(b1_layout)

        self.denominator_b0_input.setFixedWidth(80)
        self.denominator_b0_input.editingFinished.connect(lambda: self.update_coefficient(self.denominator_b0_input, "b0"))
        b0_layout = QHBoxLayout()
        b0_layout.setAlignment(Qt.AlignLeft)
        b0_layout.addWidget(QLabel("b0:"))
        b0_layout.addWidget(self.denominator_b0_input)
        b0_layout.addStretch()
        menu_view.addLayout(b0_layout)

        menu_view.addWidget(QLabel("<h3>Input signal</h3>"))
        signal_group_box = QGroupBox("Wybór sygnału pobudzającego")
        signal_layout = QVBoxLayout()

        self.sinus_button = QRadioButton("Sine wave")
        self.square_button = QRadioButton("Square signal")
        self.triangle_button = QRadioButton("Triangle wave")

        self.sinus_button.setChecked(True)

        signal_layout.addWidget(self.sinus_button)
        signal_layout.addWidget(self.square_button)
        signal_layout.addWidget(self.triangle_button)

        signal_group_box.setLayout(signal_layout)

        menu_view.addWidget(signal_group_box)
        menu_view.addWidget(set_b)
        menu_view.addWidget(back_b)


        menu_widget = QWidget()
        menu_widget.setLayout(menu_view)
        self.setCentralWidget(menu_widget)

    # tf coefficiants for easy access 
    def get_tf_coefficients(self):
        nominator = [self.a4, self.a3, self.a2, self.a1, self.a0] #licznikGÓRA
        denominator = [self.b3, self.b2, self.b1, self.b0] #mianownikDÓŁ
        return nominator, denominator

    def simulation(self):

        simulation_view= QVBoxLayout()

        title = QLabel("<h3>Symulacja układu</h3>")
        title.setAlignment(Qt.AlignCenter)

        back_b = QPushButton("Back to menu")
        back_b.clicked.connect(self.menu_display)

        simulation_view.addWidget(title)
        simulation_view.addWidget(back_b)

        simulation_widget = QWidget()
        simulation_widget.setLayout(simulation_view)
        self.setCentralWidget(simulation_widget)

        # Bode plot part

    
    
#run
if __name__ == "__main__":
    app = QApplication(sys.argv)
    windowapp = Window()
    windowapp.show()
    sys.exit(app.exec_())

"""
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

    def gain_margin():
    
    def phase_margin():
    
    def system_stability():

"""
"""class BodePlot:
    def __init__(self, nominator, denominator):
"""      
        
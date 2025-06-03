import sys
import numpy as np
import sympy as sp
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit,
    QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QRadioButton, QGroupBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from object_transfer import ObjectTransfer
from output_compute import OutputCompute
from input_function import InputFunction
from bode_plot import BodePlot
from display_functions import DisplayFunctions
        
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tf_object = ObjectTransfer()
        self.selected_signal = "sine"
        self.input_function = InputFunction(self.selected_signal)
        self.output = OutputCompute(self.selected_signal, self.tf_object, self.input_function)
        self.setWindowTitle("Transfer Function I/O Illustration")
        self.setGeometry(100, 100, 800, 800)
        self.transfer_valid = True
        self.signal_valid = True
        self.start_menu()

    def update_simulate_button_state(self):
        self.simulate_button.setEnabled(self.signal_valid)

    def update_coefficient(self, line_edit, attr_name):
        value = line_edit.text()
        try: 
            self.tf_object.update_coefficients(attr_name, value)
            self.transfer_error_label.setText("")

        except ValueError as e:
            #bad coeff corrected - given 1.0
            value = 1.0
            self.tf_object.update_coefficients(attr_name, value)
            line_edit.setText("1.0")
            self.transfer_error_label.setText(str(e))

    def update_input(self, line_edit, attr_name):
        value = line_edit.text()
        try:
            self.input_function.update_input_function(attr_name, value)
            self.signal_error_label.setText("")
            self.signal_valid = True

        except ValueError as e:
            self.signal_error_label.setText(str(e))
            self.signal_valid = False
        self.update_simulate_button_state()
    
    def update_selected_signal(self):
        if self.sine_button.isChecked():
            self.selected_signal = "sine"
            self.input_function = InputFunction("sine", 
                                            float(self.sine_amp_input.text()), 
                                            float(self.sine_freq_input.text()), 
                                            float(self.sine_phase_input.text()))
        elif self.square_button.isChecked():
            self.selected_signal = "square"
            self.input_function = InputFunction("square", 
                                            float(self.square_amp_input.text()), 
                                            float(self.square_freq_input.text()),
                                            float(self.square_phase_input.text()))
        elif self.sawtooth_button.isChecked():
            self.selected_signal = "sawtooth"
            self.input_function = InputFunction("sawtooth", 
                                            float(self.sawtooth_amp_input.text()), 
                                            float(self.sawtooth_freq_input.text()), 
                                            float(self.sawtooth_phase_input.text()))
        elif self.rec_imp_button.isChecked():
            self.selected_signal = "rectangle impulse"
            self.input_function = InputFunction("rectangle impulse", 
                                            float(self.rec_imp_amp_input.text()), 
                                            float(self.rec_imp_width_input.text()))
        elif self.triangle_button.isChecked():
            self.selected_signal = "triangle"
            self.input_function = InputFunction("triangle", 
                                            float(self.triangle_amp_input.text()), 
                                            float(self.triangle_freq_input.text()), 
                                            float(self.triangle_phase_input.text()))
        self.update_simulate_button_state()

    def _labeled_input(self, label_text, widget):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        layout.addWidget(QLabel(label_text))
        layout.addWidget(widget)
        layout.addStretch()
        return layout
    
    def update_signal_param_visibility(self):
        self.sine_params.setVisible(self.sine_button.isChecked())
        self.square_params.setVisible(self.square_button.isChecked())
        self.sawtooth_params.setVisible(self.sawtooth_button.isChecked())
        self.rec_imp_params.setVisible(self.rec_imp_button.isChecked())
        self.triangle_params.setVisible(self.triangle_button.isChecked())

    def create_latex_canvas(self, expr):
        fig, ax = plt.subplots(figsize=(6, 2), dpi=100)
        ax.axis("off")
        latex_str = r"$G(s) = " + sp.latex(expr) + r"$"
        ax.text(0.5, 0.5, latex_str, fontsize=18, ha='center', va='center')
        canvas = FigureCanvas(fig)
        return canvas

    def start_menu(self):
        layout = QVBoxLayout()
        title = QLabel("<h1>Projekt 10 - implementacja symulatora układu opisanego za pomocą transmitancji</h1>")
        title.setAlignment(Qt.AlignCenter)

        description = QLabel("Symulator umożliwia uzyskanie odpowiedzi czasowych układu na pobudzenie sygnałem" \
        " prostokątnym o nieskończonym czasie trwania, impulsem, sygnałem piłokształtnym, trójkątnym i sinusoidalnym o zadanych parametrach. Możliwa jest zmiana wszystkich" \
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
       self.numerator_a3_input = QLineEdit(str(self.tf_object.a3))
       self.numerator_a2_input = QLineEdit(str(self.tf_object.a2))
       self.numerator_a1_input = QLineEdit(str(self.tf_object.a1))
       self.numerator_a0_input = QLineEdit(str(self.tf_object.a0))
       self.denominator_b4_input = QLineEdit(str(self.tf_object.b4))
       self.denominator_b3_input = QLineEdit(str(self.tf_object.b3))
       self.denominator_b2_input = QLineEdit(str(self.tf_object.b2))
       self.denominator_b1_input = QLineEdit(str(self.tf_object.b1))
       self.denominator_b0_input = QLineEdit(str(self.tf_object.b0))
       self.set_parameters_button = QPushButton("Set parameters")
       self.simulate_button = QPushButton("Simulate")
       back_b = QPushButton("Back to start")

       self.simulate_button.clicked.connect(self.simulation)
       back_b.clicked.connect(self.start_menu)

       menu_view.addWidget(QLabel("<h3>Transfer function</h3>"))
       menu_view.addWidget(QLabel("Numerator of G :"))
       self.numerator_a3_input.setFixedWidth(80)
       self.numerator_a3_input.editingFinished.connect(lambda: self.update_coefficient(self.numerator_a3_input, "a3"))
       menu_view.addLayout(self._labeled_input("a3:", self.numerator_a3_input))

       self.numerator_a2_input.setFixedWidth(80)
       self.numerator_a2_input.editingFinished.connect(lambda: self.update_coefficient(self.numerator_a2_input, "a2"))
       menu_view.addLayout(self._labeled_input("a2:", self.numerator_a2_input))

       self.numerator_a1_input.setFixedWidth(80)
       self.numerator_a1_input.editingFinished.connect(lambda: self.update_coefficient(self.numerator_a1_input, "a1"))
       menu_view.addLayout(self._labeled_input("a1:", self.numerator_a1_input))

       self.numerator_a0_input.setFixedWidth(80)
       self.numerator_a0_input.editingFinished.connect(lambda: self.update_coefficient(self.numerator_a0_input, "a0"))
       menu_view.addLayout(self._labeled_input("a0:", self.numerator_a0_input))

       menu_view.addWidget(QLabel("Denominator of G :"))
       self.denominator_b4_input.setFixedWidth(80)
       self.denominator_b4_input.editingFinished.connect(lambda: self.update_coefficient(self.denominator_b4_input, "b4"))
       menu_view.addLayout(self._labeled_input("b4:", self.denominator_b4_input))

       self.denominator_b3_input.setFixedWidth(80)
       self.denominator_b3_input.editingFinished.connect(lambda: self.update_coefficient(self.denominator_b3_input, "b3"))
       menu_view.addLayout(self._labeled_input("b3:", self.denominator_b3_input))

       self.denominator_b2_input.setFixedWidth(80)
       self.denominator_b2_input.editingFinished.connect(lambda: self.update_coefficient(self.denominator_b2_input, "b2"))
       menu_view.addLayout(self._labeled_input("b2:", self.denominator_b2_input))

       self.denominator_b1_input.setFixedWidth(80)
       self.denominator_b1_input.editingFinished.connect(lambda: self.update_coefficient(self.denominator_b1_input, "b1"))
       menu_view.addLayout(self._labeled_input("b1:", self.denominator_b1_input))

       self.denominator_b0_input.setFixedWidth(80)
       self.denominator_b0_input.editingFinished.connect(lambda: self.update_coefficient(self.denominator_b0_input, "b0"))
       menu_view.addLayout(self._labeled_input("b0:", self.denominator_b0_input))

       menu_view.addWidget(QLabel("<h3>Input signal</h3>"))
       signal_group_box = QGroupBox("Input singnal choice")
       signal_layout = QVBoxLayout()

       self.sine_button = QRadioButton("Sine wave")
       self.square_button = QRadioButton("Square signal")
       self.sawtooth_button = QRadioButton("Sawtooth signal")
       self.rec_imp_button = QRadioButton("Rectangle impulse")
       self.triangle_button = QRadioButton("Triangle signal")

       if self.selected_signal == "sine":
            self.sine_button.setChecked(True)
       elif self.selected_signal == "square":
            self.square_button.setChecked(True)
       elif self.selected_signal == "sawtooth":
            self.sawtooth_button.setChecked(True)
       elif self.selected_signal == "rectangle impulse":
            self.rec_imp_button.setChecked(True)
       elif self.selected_signal == "triangle":
            self.triangle_button.setChecked(True)
       self.sine_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))
       self.square_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))
       self.sawtooth_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))
       self.rec_imp_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))
       self.triangle_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))

       #Sine parameters
       self.sine_params = QWidget()
       sine_layout = QVBoxLayout()
       self.sine_freq_input = QLineEdit(str(self.input_function.frequency))
       self.sine_amp_input = QLineEdit(str(self.input_function.amplitude))
       self.sine_phase_input = QLineEdit(str(self.input_function.phase))
       for w in [self.sine_freq_input, self.sine_amp_input, self.sine_phase_input]:
           w.setFixedWidth(80)
           w.setAlignment(Qt.AlignLeft)
       self.sine_freq_input.editingFinished.connect(lambda: self.update_input(self.sine_freq_input, "frequency"))
       self.sine_amp_input.editingFinished.connect(lambda: self.update_input(self.sine_amp_input, "amplitude"))
       self.sine_phase_input.editingFinished.connect(lambda: self.update_input(self.sine_phase_input, "phase"))
       sine_layout.addLayout(self._labeled_input("Frequency [Hz]:", self.sine_freq_input))
       sine_layout.addLayout(self._labeled_input("Amplitude [V]:", self.sine_amp_input))
       sine_layout.addLayout(self._labeled_input("Phase [rad]:", self.sine_phase_input))
       self.sine_params.setLayout(sine_layout)

       #Square parameters
       self.square_params = QWidget()
       square_layout = QVBoxLayout()
       self.square_freq_input = QLineEdit(str(self.input_function.frequency))
       self.square_amp_input = QLineEdit(str(self.input_function.amplitude))
       self.square_phase_input = QLineEdit(str(self.input_function.phase))
       for w in [self.square_freq_input, self.square_amp_input, self.square_phase_input]:
           w.setFixedWidth(80)
           w.setAlignment(Qt.AlignLeft)
       self.square_freq_input.editingFinished.connect(lambda: self.update_input(self.square_freq_input, "frequency"))
       self.square_amp_input.editingFinished.connect(lambda: self.update_input(self.square_amp_input, "amplitude"))
       self.square_phase_input.editingFinished.connect(lambda: self.update_input(self.square_phase_input, "phase"))
       square_layout.addLayout(self._labeled_input("Frequency [Hz]:", self.square_freq_input))
       square_layout.addLayout(self._labeled_input("Amplitude [V]:", self.square_amp_input))
       square_layout.addLayout(self._labeled_input("Phase [rad]:", self.square_phase_input))
       self.square_params.setLayout(square_layout)

       #Sawtooth params
       self.sawtooth_params = QWidget()
       sawtooth_layout = QVBoxLayout()
       self.sawtooth_freq_input = QLineEdit(str(self.input_function.frequency))
       self.sawtooth_amp_input = QLineEdit(str(self.input_function.amplitude))
       self.sawtooth_phase_input = QLineEdit(str(self.input_function.phase))
       for w in [self.sawtooth_freq_input, self.sawtooth_amp_input, self.sawtooth_phase_input]:
           w.setFixedWidth(80)
           w.setAlignment(Qt.AlignLeft)
       self.sawtooth_freq_input.editingFinished.connect(lambda: self.update_input(self.sawtooth_freq_input, "frequency"))
       self.sawtooth_amp_input.editingFinished.connect(lambda: self.update_input(self.sawtooth_amp_input, "amplitude"))
       self.sawtooth_phase_input.editingFinished.connect(lambda: self.update_input(self.sawtooth_phase_input, "phase"))
       sawtooth_layout.addLayout(self._labeled_input("Frequency [Hz]:", self.sawtooth_freq_input))
       sawtooth_layout.addLayout(self._labeled_input("Amplitude [V]:", self.sawtooth_amp_input))
       sawtooth_layout.addLayout(self._labeled_input("Phase [rad]:", self.sawtooth_phase_input))
       self.sawtooth_params.setLayout(sawtooth_layout)

       #Rectangle impulse params
       self.rec_imp_params = QWidget()
       rec_imp_layout = QVBoxLayout()
       self.rec_imp_amp_input = QLineEdit(str(self.input_function.amplitude))
       self.rec_imp_width_input = QLineEdit(str(self.input_function.pulse_width))
       for w in [self.rec_imp_amp_input, self.rec_imp_width_input]:
           w.setFixedWidth(80)
           w.setAlignment(Qt.AlignLeft)
       self.rec_imp_amp_input.editingFinished.connect(lambda: self.update_input(self.rec_imp_amp_input, "amplitude"))
       self.rec_imp_width_input.editingFinished.connect(lambda: self.update_input(self.rec_imp_width_input, "pulse_width"))
       rec_imp_layout.addLayout(self._labeled_input("Amplitude [V]:", self.rec_imp_amp_input))
       rec_imp_layout.addLayout(self._labeled_input("Pulse width [s]:", self.rec_imp_width_input))
       self.rec_imp_params.setLayout(rec_imp_layout)

       #Triangle params
       self.triangle_params = QWidget()
       triangle_layout = QVBoxLayout()
       self.triangle_freq_input = QLineEdit(str(self.input_function.frequency))
       self.triangle_amp_input = QLineEdit(str(self.input_function.amplitude))
       self.triangle_phase_input = QLineEdit(str(self.input_function.phase))
       for w in [self.triangle_freq_input, self.triangle_amp_input, self.triangle_phase_input]:
           w.setFixedWidth(80)
           w.setAlignment(Qt.AlignLeft)
       self.triangle_freq_input.editingFinished.connect(lambda: self.update_input(self.triangle_freq_input, "frequency"))
       self.triangle_amp_input.editingFinished.connect(lambda: self.update_input(self.triangle_amp_input, "amplitude"))
       self.triangle_phase_input.editingFinished.connect(lambda: self.update_input(self.triangle_phase_input, "phase"))
       triangle_layout.addLayout(self._labeled_input("Frequency [Hz]:", self.triangle_freq_input))
       triangle_layout.addLayout(self._labeled_input("Amplitude [V]:", self.triangle_amp_input))
       triangle_layout.addLayout(self._labeled_input("Phase [rad]:", self.triangle_phase_input))
       self.triangle_params.setLayout(triangle_layout)

       signal_layout.addWidget(self.sine_button)
       signal_layout.addWidget(self.sine_params)
       signal_layout.addWidget(self.square_button)
       signal_layout.addWidget(self.square_params)
       signal_layout.addWidget(self.sawtooth_button)
       signal_layout.addWidget(self.sawtooth_params)
       signal_layout.addWidget(self.rec_imp_button)
       signal_layout.addWidget(self.rec_imp_params)
       signal_layout.addWidget(self.triangle_button)
       signal_layout.addWidget(self.triangle_params)

       signal_group_box.setLayout(signal_layout)
       menu_view.addWidget(signal_group_box)

       #Show only selected signal parameters
       self.update_signal_param_visibility()

       menu_view.addWidget(self.set_parameters_button)
       menu_view.addWidget(self.simulate_button)
       menu_view.addWidget(back_b)

       menu_widget = QWidget()
       menu_widget.setLayout(menu_view)
       self.setCentralWidget(menu_widget)

       self.signal_error_label = QLabel("")
       self.signal_error_label.setStyleSheet("color: red")
       self.transfer_error_label = QLabel("")
       self.transfer_error_label.setStyleSheet("color: red")
       menu_view.addWidget(self.transfer_error_label)
       menu_view.addWidget(self.signal_error_label)


    def simulation(self):

        simulation_view= QVBoxLayout()

        title = QLabel("<h3>Simulation</h3>")
        title.setAlignment(Qt.AlignCenter)

        back_b = QPushButton("Back to menu")
        back_b.clicked.connect(self.menu_display)
        simulation_view.addWidget(title)
        simulation_widget = QWidget()
        simulation_widget.setLayout(simulation_view)
        self.setCentralWidget(simulation_widget)

        try:
            self.bode = BodePlot(self.tf_object)
            simulation_view.addWidget(self.bode.canvas)

            stability = QLabel(f"Stable system: {self.bode.stable}")
            stability.setAlignment(Qt.AlignCenter) 
            simulation_view.addWidget(stability)
        
        except ValueError as e:
            error_label = QLabel(f"Error: {e}")
            error_label.setStyleSheet("color: red")
            simulation_view.addWidget(error_label)

        canvas = self.create_latex_canvas(self.tf_object.get_symbolic_tf())
        simulation_view.addWidget(canvas)

        simulation_view.addWidget(self.input_function.input_plot())
        simulation_view.addWidget(self.output.output_plot())
        simulation_view.addWidget(back_b)
          
#run
if __name__ == "__main__":
    app = QApplication(sys.argv)
    windowapp = Window()
    windowapp.show()
    sys.exit(app.exec_())


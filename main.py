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
        
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tf_object = ObjectTransfer()
        self.selected_signal = "sine"
        self.input_function = InputFunction(self.selected_signal)
        self.output = OutputCompute(self.selected_signal, self.tf_object, self.input_function)
        self.setWindowTitle("Transfer Function I/O Illustration")
        self.setGeometry(100, 100, 800, 800)
        self.start_menu()

    def check_input_values(self):
        if self.check_transfer_values() == False:
            self.error_label.setText("Wrong transfer function")
            self.error_label.setStyleSheet("color: red")
            return False
        
        numerator, denominator = self.tf_object.get_tf_coefficients()
        all_floats = all(isinstance(c, float) for c in numerator + denominator)
        correct_num = any(coef != 0 for coef in numerator)
        correct_den = any(coef != 0 for coef in denominator)
        if not correct_num or not correct_den or not all_floats:
            self.error_label.setText("Wrong transfer function")
            self.error_label.setStyleSheet("color: red")
            return False
        
        order_num, order_den = self.tf_object.get_system_order()
        if order_num>order_den:
            self.error_label.setText("Wrong transfer function")
            self.error_label.setStyleSheet("color: red")
            return False

        try:
            if self.selected_signal in ["sine", "square"]:
                freq = float(self.sine_freq_input.text() if self.selected_signal == "sine" else self.square_freq_input.text())
                amp = float(self.sine_amp_input.text() if self.selected_signal == "sine" else self.square_amp_input.text())
                phase = float(self.sine_phase_input.text() if self.selected_signal == "sine" else self.square_phase_input.text())
                if freq <= 0:
                    raise ValueError("Frequency must be positive.")
                if amp <= 0:
                    raise ValueError("Amplitude must be positive.")
                if not (-np.pi <= phase <= np.pi):
                    raise ValueError("Phase must be in [-π, π].")
                self.input_function.amplitude = amp
                self.input_function.frequency = freq
                self.input_function.phase = phase
                
            elif self.selected_signal == "sawtooth":
                freq = float(self.sawtooth_freq_input.text())
                amp = float(self.sawtooth_amp_input.text())
                if freq <= 0:
                    raise ValueError("Frequency must be positive.")
                if amp <= 0:
                    raise ValueError("Amplitude must be positive.")
                self.input_function.amplitude = amp
                self.input_function.frequency = freq

            elif self.selected_signal == "rectangle impulse":
                amp = float(self.rec_imp_amp_input.text())
                width = float(self.rec_imp_width_input.text())
                if amp <= 0:
                    raise ValueError("Amplitude must be positive.")
                if width <= 0:
                    raise ValueError("Pulse width must be positive.")
                self.input_function.amplitude = amp
                self.input_function.pulse_width = width

            elif self.selected_signal == "triangle":
                freq = float(self.triangle_freq_input.text())
                amp = float(self.triangle_amp_input.text())
                if freq <= 0:
                    raise ValueError("Frequency must be positive.")
                if amp <= 0:
                    raise ValueError("Amplitude must be positive.")
                self.input_function.amplitude = amp
                self.input_function.frequency = freq

            elif self.selected_signal in ["impulse", "step"]:
                amp = float(self.impulse_amp_input.text() if self.selected_signal == "impulse" else self.step_amp_input.text())
                if amp <= 0:
                    raise ValueError("Amplitude must be positive.")
                self.input_function.amplitude = amp

        except ValueError as e:
            self.error_label.setText(str(e))
            self.error_label.setStyleSheet("color: red")
            return False

        self.error_label.setText("Correct parameters")  
        self.error_label.setStyleSheet("color: green")
        return True
    
    def check_transfer_values(self):
        try:
            inputs = {
                self.numerator_a3_input: "a3",
                self.numerator_a2_input: "a2",
                self.numerator_a1_input: "a1",
                self.numerator_a0_input: "a0",
                self.denominator_b4_input: "b4",
                self.denominator_b3_input: "b3",
                self.denominator_b2_input: "b2",
                self.denominator_b1_input: "b1",
                self.denominator_b0_input: "b0"
            }

            for input_field, coeff_name in inputs.items():
                text = input_field.text()
                value = float(text) 
                setattr(self.tf_object, coeff_name, value)
            return True  

        except ValueError:
            return False  

    def check_and_simulate(self):
        if self.check_input_values():
            self.simulation()
    
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
                                            float(self.sawtooth_freq_input.text()))
        elif self.rec_imp_button.isChecked():
            self.selected_signal = "rectangle impulse"
            self.input_function = InputFunction("rectangle impulse", 
                                            float(self.rec_imp_amp_input.text()), 
                                            float(self.rec_imp_width_input.text()))
        elif self.triangle_button.isChecked():
            self.selected_signal = "triangle"
            self.input_function = InputFunction("triangle", 
                                            float(self.triangle_amp_input.text()), 
                                            float(self.triangle_freq_input.text()))
        elif self.impulse_button.isChecked():
            self.selected_signal = "impulse"
            self.input_function = InputFunction("impulse", 
                                            float(self.impulse_amp_input.text()))
        elif self.step_button.isChecked():
            self.selected_signal = "step"
            self.input_function = InputFunction("step", 
                                            float(self.step_amp_input.text()))
    
    def update_signal_param_visibility(self):
        self.sine_params.setVisible(self.sine_button.isChecked())
        self.square_params.setVisible(self.square_button.isChecked())
        self.sawtooth_params.setVisible(self.sawtooth_button.isChecked())
        self.rec_imp_params.setVisible(self.rec_imp_button.isChecked())
        self.triangle_params.setVisible(self.triangle_button.isChecked())
        self.impulse_params.setVisible(self.impulse_button.isChecked())
        self.step_params.setVisible(self.step_button.isChecked())

    def _labeled_input(self, label_text, widget):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        layout.addWidget(QLabel(label_text))
        layout.addWidget(widget)
        layout.addStretch()
        return layout

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
        " prostokątnym o nieskończonym czasie trwania, impulsem prostokątnym, skokiem jednostkowym, impulsem jednostkowym, sygnałem piłokształtnym," \
        " trójkątnym i sinusoidalnym o zadanych parametrach. Możliwa jest zmiana wszystkich" \
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

       self.error_label = QLabel("")
       self.error_label.setAlignment(Qt.AlignLeft)

       self.set_parameters_button.clicked.connect(self.check_input_values)
       self.simulate_button.clicked.connect(self.check_and_simulate)
       back_b.clicked.connect(self.start_menu)

       menu_view.addWidget(QLabel("<h3>Transfer function</h3>"))
       menu_view.addWidget(QLabel("Numerator of G :"))
       self.numerator_a3_input.setFixedWidth(80) 
       menu_view.addLayout(self._labeled_input("a3:", self.numerator_a3_input))
       self.numerator_a2_input.setFixedWidth(80)
       menu_view.addLayout(self._labeled_input("a2:", self.numerator_a2_input))
       self.numerator_a1_input.setFixedWidth(80)
       menu_view.addLayout(self._labeled_input("a1:", self.numerator_a1_input))
       self.numerator_a0_input.setFixedWidth(80)
       menu_view.addLayout(self._labeled_input("a0:", self.numerator_a0_input))

       menu_view.addWidget(QLabel("Denominator of G :"))
       self.denominator_b4_input.setFixedWidth(80)
       menu_view.addLayout(self._labeled_input("b4:", self.denominator_b4_input))
       self.denominator_b3_input.setFixedWidth(80)
       menu_view.addLayout(self._labeled_input("b3:", self.denominator_b3_input))
       self.denominator_b2_input.setFixedWidth(80)
       menu_view.addLayout(self._labeled_input("b2:", self.denominator_b2_input))
       self.denominator_b1_input.setFixedWidth(80)
       menu_view.addLayout(self._labeled_input("b1:", self.denominator_b1_input))
       self.denominator_b0_input.setFixedWidth(80)
       menu_view.addLayout(self._labeled_input("b0:", self.denominator_b0_input))

       menu_view.addWidget(QLabel("<h3>Input signal</h3>"))
       signal_group_box = QGroupBox("Input singnal choice")
       signal_layout = QVBoxLayout()

       self.sine_button = QRadioButton("Sine wave")
       self.square_button = QRadioButton("Square signal")
       self.sawtooth_button = QRadioButton("Sawtooth signal")
       self.rec_imp_button = QRadioButton("Rectangle impulse")
       self.triangle_button = QRadioButton("Triangle signal")
       self.impulse_button = QRadioButton("Impulse")
       self.step_button = QRadioButton("Step")
      
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
       elif self.selected_signal == "impulse":
            self.impulse_button.setChecked(True)
       elif self.selected_signal == "step":
            self.step_button.setChecked(True)
       self.sine_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))
       self.square_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))
       self.sawtooth_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))
       self.rec_imp_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))
       self.triangle_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))
       self.impulse_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))
       self.step_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))
    
       #Sine parameters
       self.sine_params = QWidget()
       sine_layout = QVBoxLayout()
       self.sine_freq_input = QLineEdit(str(self.input_function.frequency))
       self.sine_amp_input = QLineEdit(str(self.input_function.amplitude))
       self.sine_phase_input = QLineEdit(str(self.input_function.phase))
       for w in [self.sine_freq_input, self.sine_amp_input, self.sine_phase_input]:
           w.setFixedWidth(80)
           w.setAlignment(Qt.AlignLeft)
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
       square_layout.addLayout(self._labeled_input("Frequency [Hz]:", self.square_freq_input))
       square_layout.addLayout(self._labeled_input("Amplitude [V]:", self.square_amp_input))
       square_layout.addLayout(self._labeled_input("Phase [rad]:", self.square_phase_input))
       self.square_params.setLayout(square_layout)

       #Sawtooth parameters
       self.sawtooth_params = QWidget()
       sawtooth_layout = QVBoxLayout()
       self.sawtooth_freq_input = QLineEdit(str(self.input_function.frequency))
       self.sawtooth_amp_input = QLineEdit(str(self.input_function.amplitude))
       for w in [self.sawtooth_freq_input, self.sawtooth_amp_input]:
           w.setFixedWidth(80)
           w.setAlignment(Qt.AlignLeft)
       sawtooth_layout.addLayout(self._labeled_input("Frequency [Hz]:", self.sawtooth_freq_input))
       sawtooth_layout.addLayout(self._labeled_input("Amplitude [V]:", self.sawtooth_amp_input))
       self.sawtooth_params.setLayout(sawtooth_layout)

       #Rectangle impulse parameters
       self.rec_imp_params = QWidget()
       rec_imp_layout = QVBoxLayout()
       self.rec_imp_amp_input = QLineEdit(str(self.input_function.amplitude))
       self.rec_imp_width_input = QLineEdit(str(self.input_function.pulse_width))
       for w in [self.rec_imp_amp_input, self.rec_imp_width_input]:
           w.setFixedWidth(80)
           w.setAlignment(Qt.AlignLeft)
       rec_imp_layout.addLayout(self._labeled_input("Amplitude [V]:", self.rec_imp_amp_input))
       rec_imp_layout.addLayout(self._labeled_input("Pulse width [s]:", self.rec_imp_width_input))
       self.rec_imp_params.setLayout(rec_imp_layout)

       #Triangle parameters
       self.triangle_params = QWidget()
       triangle_layout = QVBoxLayout()
       self.triangle_freq_input = QLineEdit(str(self.input_function.frequency))
       self.triangle_amp_input = QLineEdit(str(self.input_function.amplitude))
       for w in [self.triangle_freq_input, self.triangle_amp_input]:
           w.setFixedWidth(80)
           w.setAlignment(Qt.AlignLeft)
       triangle_layout.addLayout(self._labeled_input("Frequency [Hz]:", self.triangle_freq_input))
       triangle_layout.addLayout(self._labeled_input("Amplitude [V]:", self.triangle_amp_input))
       self.triangle_params.setLayout(triangle_layout)

       #Impulse parameters
       self.impulse_params = QWidget()
       impulse_layout = QVBoxLayout()
       self.impulse_amp_input = QLineEdit(str(self.input_function.amplitude))
       for w in [self.impulse_amp_input]:
           w.setFixedWidth(80)
           w.setAlignment(Qt.AlignLeft)
       impulse_layout.addLayout(self._labeled_input("Amplitude [V]:", self.impulse_amp_input))
       self.impulse_params.setLayout(impulse_layout)

       #Step parameters
       self.step_params = QWidget()
       step_layout = QVBoxLayout()
       self.step_amp_input = QLineEdit(str(self.input_function.amplitude))
       for w in [self.step_amp_input]:
           w.setFixedWidth(80)
           w.setAlignment(Qt.AlignLeft)
       step_layout.addLayout(self._labeled_input("Amplitude [V]:", self.step_amp_input))
       self.step_params.setLayout(step_layout)


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
       signal_layout.addWidget(self.impulse_button)
       signal_layout.addWidget(self.impulse_params)
       signal_layout.addWidget(self.step_button)
       signal_layout.addWidget(self.step_params)

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

       menu_view.addWidget(self.error_label)


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

        self.bode = BodePlot(self.tf_object)
        simulation_view.addWidget(self.bode.canvas)

        stability = QLabel(f"Stable system: {self.bode.stable}")
        stability.setAlignment(Qt.AlignCenter) 
        simulation_view.addWidget(stability)

        canvas = self.create_latex_canvas(self.tf_object.get_symbolic_tf())
        simulation_view.addWidget(canvas)

        self.output = OutputCompute(self.selected_signal, self.tf_object, self.input_function)

        simulation_view.addWidget(self.input_function.input_plot())
        simulation_view.addWidget(self.output.output_plot())
        simulation_view.addWidget(back_b)
          
#run
if __name__ == "__main__":
    app = QApplication(sys.argv)
    windowapp = Window()
    windowapp.show()
    sys.exit(app.exec_())


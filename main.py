import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit,
    QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QRadioButton, QGroupBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.signal import TransferFunction
from scipy.signal import freqs


class ObjectTransfer:
    def __init__(self):
      self.b4 = 0.0
      self.b3 = 0.0
      self.b2 = 1.0
      self.b1 = 1.0
      self.b0 = 1.0
      self.a3 = 0.0
      self.a2 = 0.0
      self.a1 = 1.0
      self.a0 = 1.0

    def get_tf_coefficients(self):
      numerator = [self.a3, self.a2, self.a1, self.a0]
      denominator = [self.b3, self.b2, self.b1, self.b0]
      return numerator, denominator
    
    def update_coefficients(self, attr_name, value):
       try:
            value = float(value)
       except ValueError:
            raise ValueError(f"{attr_name.capitalize()} musi być liczbą.")
       setattr(self, attr_name, value)
        
    def correct_values(self):
      numerator, denominator = self.get_tf_coefficients()
      all_floats = all(isinstance(c, float) for c in numerator + denominator)
      correct_num = any(coef != 0 for coef in numerator)
      correct_den = any(coef != 0 for coef in denominator)
      return correct_num and correct_den and all_floats
    
    def get_tf(self):
        if not self.correct_values():
            raise ValueError("Nieprawidłowa transmitancja obiektu")
        num, den = self.get_tf_coefficients()
        return TransferFunction(num, den)
    
    def zeros_and_poles(self):
      #get the poles and zeros 
      tf = self.get_tf()
      return list(tf.zeros), list(tf.poles)
    
"""class OutputCompute:
    def __init__(self, signal_type, tf_object):
        self.sine = InputSineFunction()
        self.square = InputSquareFunction()
        self.triangle = InputTrianfleFunction()
        self.tf_object = tf_object
        if signal_type == "sine":
            self.num_u, self.den_u = self.sine.sine_transfer()
        elif signal_type == "square":
            self.num_u, self.den_u = self.square.square_transfer()
        elif signal_type == "triangle":
            self.num_u, self.den_u = self.triangle.triangle_transfer()
        else:
            raise ValueError("Unknown signal type")
        
    def compute_Y(self):
        num_G, den_G  = self.tf_object.get_tf_coefficients()
        num_U, den_U = self.num_u, self.den_u

        #transfer function of Y
        num_Y = np.polymul(num_g, num_u)
        den_Y = np.polymul(den_g, den_u)
        system = TransferFunction(num_Y, den_Y)

    def differentation_rk4(self):
        
    def output_plot(self):


class InputSquareFunction:
    def __init__(self, signal_type="square"):
        self.signal_type = signal_type
    
    def square_transfer_function(self):
        return square_transfer
    
    def square_input_plot(self):

class InputTriangleFunction:
    def __init__(self, signal_type="triangle"):
        self.signal_type = signal_type
        
    def triangle_transfer(self):
        return triagnle_transfer
        
    def triangle_input_plot(self):"""
    
class InputSineFunction:
    def __init__(self, signal_type="sine", amplitude=1.0, frequency=1.0, phase=0.0):
        self.signal_type = signal_type
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    def update_sine(self, attr_name, value):
        try:
            value = float(value)
        except ValueError:
            raise ValueError(f"{attr_name.capitalize()} musi być liczbą.")
 
        if attr_name == "frequency" and value <= 0:
            raise ValueError("Częstotliwość musi być większa niż zero.")
        if attr_name == "amplitude" and value <= 0:
            raise ValueError("Amplituda musi być większa niż zero.")
        if attr_name == "phase" and not (-np.pi <= value <= np.pi):
            raise ValueError("Faza musi być w zakresie od -π do +π.")

        setattr(self, attr_name, value)

    """def sine_transfer_function(self):
        sine_transfer =  #tu bedzie transmitancja sinusa
        return sine_transfer
        
        def sine_input_plot(self):"""

       
# Plotting the Bode
class BodePlot:
    def __init__(self, tf_object):
      self.tf_object = tf_object
      self.numerator, self.denominator = self.tf_object.get_tf_coefficients()
      zeros, poles = self.tf_object.zeros_and_poles()

      #Zero is bad at log scale
      zeros_and_poles = [abs(f) for f in zeros + poles if abs(f) > 1e-6]

     # preparing range of the plot
      if zeros_and_poles:
        min_value = 0.1 * min(zeros_and_poles)
        max_value = 10 * max(zeros_and_poles)
      else:
        min_value = 0.1
        max_value = 100
      
      #the necessary range of the plot
      self.range = [min_value, max_value]
      self.figure = Figure(figsize=(6, 4))
      self.canvas = FigureCanvas(self.figure)
      self.plotting_bode()
    
    def plotting_bode(self):
        ax_mag = self.figure.add_subplot(211)
        ax_ph = self.figure.add_subplot(212, sharex=ax_mag) #rows,col,index
        
        # w to put in tf
        w = np.logspace(np.log10(self.range[0]), np.log10(self.range[1]), 1000) # 1000 points to count
        
        # counts tf(j*w)
        w, plot_line = freqs(self.numerator, self.denominator,w)

        #change to dB and angle respectively
        magnitude = 20 * np.log10(abs(plot_line))
        phase = np.angle(plot_line, deg=True)
        
        #STABILITY
        to_zero = np.abs(phase + 180) #we're looking for phase at -180 so minimazing it to 0
        phase_180_idx = np.argmin(to_zero)
        magnitude_180 = magnitude[phase_180_idx]
        gain_margin = -magnitude_180 #zapas wzmocnienia

        gain_0_idx = np.argmin(np.abs(magnitude))
        phase_0 = phase[gain_0_idx]
        phase_margin = 180 + phase_0   

        if gain_margin and phase_margin > 0:
            self.stable = True
        else:
            self.stable = False

        #Plotting magnitude
        ax_mag.set_title("Magnitude Bode Plot")
        ax_mag.set_xlabel("Frequency [rad/s]")
        ax_mag.set_ylabel("Magnitude [dB]")
        ax_mag.set_xscale("log") # log on x axis
        ax_mag.plot(w, magnitude)

        #PLotting phase
        ax_ph.set_title("Phase Bode Plot")
        ax_ph.set_xlabel("Frequency [rad/s]")
        ax_ph.set_ylabel("Phase [°]")
        ax_ph.set_xscale("log") # log on x axis
        ax_ph.plot(w, phase)

        self.canvas.draw()
      

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tf_object = ObjectTransfer()
        self.sine_function = InputSineFunction()
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


    def update_sine(self, line_edit, attr_name):
        value = line_edit.text()
        try:
            self.sine_function.update_sine(attr_name, value)
            self.signal_error_label.setText("")
            self.signal_valid = True

        except ValueError as e:
            self.signal_error_label.setText(str(e))
            self.signal_valid = False
        self.update_simulate_button_state()

    def update_selected_signal(self):
        if self.sine_button.isChecked():
            self.selected_signal = "sine"
        elif self.square_button.isChecked():
            self.selected_signal = "square"
        elif self.triangle_button.isChecked():
            self.selected_signal = "triangle"

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
        self.triangle_params.setVisible(self.triangle_button.isChecked())

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

        self.selected_signal = "sine"

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
       signal_group_box = QGroupBox("Wybór sygnału pobudzającego")
       signal_layout = QVBoxLayout()

       self.sine_button = QRadioButton("Sine wave")
       self.square_button = QRadioButton("Square signal")
       self.triangle_button = QRadioButton("Triangle wave")

       if self.selected_signal == "sine":
            self.sine_button.setChecked(True)
       elif self.selected_signal == "square":
            self.square_button.setChecked(True)
       elif self.selected_signal == "triangle":
            self.triangle_button.setChecked(True)
       self.sine_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))
       self.square_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))
       self.triangle_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))

       #Sine parameters
       self.sine_params = QWidget()
       sine_layout = QVBoxLayout()
       self.freq_input = QLineEdit(str(self.sine_function.frequency))
       self.amp_input = QLineEdit(str(self.sine_function.amplitude))
       self.phase_input = QLineEdit(str(self.sine_function.phase))
       for w in [self.freq_input, self.amp_input, self.phase_input]:
           w.setFixedWidth(80)
           w.setAlignment(Qt.AlignLeft)
       self.freq_input.editingFinished.connect(lambda: self.update_sine(self.freq_input, "frequency"))
       self.amp_input.editingFinished.connect(lambda: self.update_sine(self.amp_input, "amplitude"))
       self.phase_input.editingFinished.connect(lambda: self.update_sine(self.phase_input, "phase"))
       sine_layout.addLayout(self._labeled_input("Częstotliwość [Hz]:", self.freq_input))
       sine_layout.addLayout(self._labeled_input("Amplituda [V]:", self.amp_input))
       sine_layout.addLayout(self._labeled_input("Przesunięcie fazowe [rad]:", self.phase_input))
       self.sine_params.setLayout(sine_layout)

       #Square parameters
       self.square_params = QWidget()
       square_layout = QVBoxLayout()
       self.square_amp_input = QLineEdit("1.0")
       self.square_freq_input = QLineEdit("1.0")
       self.square_amp_input.setFixedWidth(80)
       self.square_freq_input.setFixedWidth(80)
       square_layout.addLayout(self._labeled_input("Amplituda [V]:", self.square_amp_input))
       square_layout.addLayout(self._labeled_input("Częstotliwość [Hz]:", self.square_freq_input))
       self.square_params.setLayout(square_layout)

       #Triangle params
       self.triangle_params = QWidget()
       triangle_layout = QVBoxLayout()
       self.triangle_amp_input = QLineEdit("1.0")
       self.triangle_freq_input = QLineEdit("1.0")
       self.triangle_amp_input.setFixedWidth(80)
       self.triangle_freq_input.setFixedWidth(80)
       triangle_layout.addLayout(self._labeled_input("Amplituda [V]:", self.triangle_amp_input))
       triangle_layout.addLayout(self._labeled_input("Częstotliwość [Hz]:", self.triangle_freq_input))
       self.triangle_params.setLayout(triangle_layout)

       signal_layout.addWidget(self.sine_button)
       signal_layout.addWidget(self.sine_params)
       signal_layout.addWidget(self.square_button)
       signal_layout.addWidget(self.square_params)
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

        title = QLabel("<h3>Symulacja układu</h3>")
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

            stability = QLabel(f"System stabilny: {self.bode.stable}")
            stability.setAlignment(Qt.AlignCenter) 
            simulation_view.addWidget(stability)
        
        except ValueError as e:
            error_label = QLabel(f"Błąd: {e}")
            error_label.setStyleSheet("color: red")
            simulation_view.addWidget(error_label)

        simulation_view.addWidget(back_b)
          
#run
if __name__ == "__main__":
    app = QApplication(sys.argv)
    windowapp = Window()
    windowapp.show()
    sys.exit(app.exec_())

     

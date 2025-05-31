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
from scipy.signal import sawtooth
from scipy.signal import fftconvolve


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
            raise ValueError(f"{attr_name.capitalize()} must be a number.")
       setattr(self, attr_name, value)
        
    def correct_values(self):
      numerator, denominator = self.get_tf_coefficients()
      all_floats = all(isinstance(c, float) for c in numerator + denominator)
      correct_num = any(coef != 0 for coef in numerator)
      correct_den = any(coef != 0 for coef in denominator)
      return correct_num and correct_den and all_floats
      #SPRAWDZANIE CZY TRANSMITANCJA JEST WŁAŚCIWA(?)
    
    def get_tf(self):
        if not self.correct_values():
            raise ValueError("Incorrect transfer function")
        num, den = self.get_tf_coefficients()
        return TransferFunction(num, den)
    
    def zeros_and_poles(self):
      #get the poles and zeros 
      tf = self.get_tf()
      return list(tf.zeros), list(tf.poles)
    

"""class OutputCompute:
    def __init__(self, signal_type, tf_object, input):
        self.input = input
        self.tf_object = tf_object

    #input in time domain
    def input_u_t(self):
        self.u, self.t = input.input_generate()
    
    def differentation_rk4(self):
        
    def output_plot(self):"""


"""class InputSquareFunction:
    def __init__(self, signal_type="square"):
        self.signal_type = signal_type
    
    def square_transfer_function(self):
        return square_transfer
    
    def square_input_plot(self):"""

class InputFunction:
    def __init__(self, signal_type, amplitude=1.0, frequency=1.0, phase=0.0, duration=2.0, sample_rate=1000):
        self.signal_type = signal_type
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.duration = duration
        self.sample_rate = sample_rate

    def update_input_function(self, attr_name, value):
        try:
            value = float(value)
        except ValueError:
            raise ValueError(f"{attr_name.capitalize()} must be a number.")
 
        if attr_name == "frequency" and value <= 0:
            raise ValueError("Wrong frequency.")
        if attr_name == "amplitude" and value <= 0:
            raise ValueError("Wrong amplitude.")
        if attr_name == "phase" and not (-np.pi <= value <= np.pi):
            raise ValueError("Wrong phase [-pi,pi].")
        setattr(self, attr_name, value)

    def input_generate(self):
        if self.signal_type == "sawtooth":
            t = np.linspace(0, self.duration, int(self.duration * self.sample_rate), endpoint=False)
            y = self.amplitude * sawtooth(2 * np.pi * self.frequency * t + self.phase)
            return t,y
        elif self.signal_type == "sine":
            t = np.linspace(0, self.duration, int(self.duration * self.sample_rate), endpoint=False)
            y = self.amplitude * np.sin(2 * np.pi * self.frequency * t + self.phase)
            return t, y

    def input_plot(self):
        t, y = self.input_generate()
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        ax = self.figure.add_subplot(111)  

        ax.plot(t, y)
        ax.set_title(f"Input {self.signal_type} signal")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude")
        ax.grid(True)
        self.canvas.draw()
        return self.canvas        
        
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
        self.selected_signal = "sine"
        self.input_function = InputFunction(self.selected_signal)
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
                                            float(self.square_freq_input.text()))
        elif self.sawtooth_button.isChecked():
            self.selected_signal = "sawtooth"
            self.input_function = InputFunction("sawtooth", 
                                            float(self.sawtooth_amp_input.text()), 
                                            float(self.sawtooth_freq_input.text()), 
                                            float(self.sawtooth_phase_input.text()))

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
       signal_group_box = QGroupBox("Input singnal choice")
       signal_layout = QVBoxLayout()

       self.sine_button = QRadioButton("Sine wave")
       self.square_button = QRadioButton("Square signal")
       self.sawtooth_button = QRadioButton("Sawtooth signal")

       if self.selected_signal == "sine":
            self.sine_button.setChecked(True)
       elif self.selected_signal == "square":
            self.square_button.setChecked(True)
       elif self.selected_signal == "sawtooth":
            self.sawtooth_button.setChecked(True)
       self.sine_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))
       self.square_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))
       self.sawtooth_button.toggled.connect(lambda: (self.update_selected_signal(), self.update_signal_param_visibility()))

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
       """self.square_freq_input = QLineEdit(str(self.square_function.frequency))
       self.square_amp_input = QLineEdit(str(self.square_function.amplitude))
       self.square_phase_input = QLineEdit(str(self.square_function.phase))
       for w in [self.square_freq_input, self.square_amp_input, self.square_phase_input]:
           w.setFixedWidth(80)
           w.setAlignment(Qt.AlignLeft)
       self.square_freq_input.editingFinished.connect(lambda: self.update_square(self.square_freq_input, "frequency"))
       self.square_amp_input.editingFinished.connect(lambda: self.update_square(self.square_amp_input, "amplitude"))
       self.square_phase_input.editingFinished.connect(lambda: self.update_square(self.square_phase_input, "phase"))
       square_layout.addLayout(self._labeled_input("Amplitude [V]:", self.square_amp_input))
       square_layout.addLayout(self._labeled_input("Frequency [Hz]:", self.square_freq_input))
       square_layout.addLayout(self._labeled_input("Phase [rad]:", self.square_phase_input))"""
       self.square_amp_input = QLineEdit("1.0")
       self.square_freq_input = QLineEdit("1.0")
       self.square_amp_input.setFixedWidth(80)
       self.square_freq_input.setFixedWidth(80)
       square_layout.addLayout(self._labeled_input("Amplitude [V]:", self.square_amp_input))
       square_layout.addLayout(self._labeled_input("Frequency [Hz]:", self.square_freq_input))
       self.square_params.setLayout(square_layout)

       #Triangle params
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
       sawtooth_layout.addLayout(self._labeled_input("Amplitude [V]:", self.sawtooth_amp_input))
       sawtooth_layout.addLayout(self._labeled_input("Frequency [Hz]:", self.sawtooth_freq_input))
       sawtooth_layout.addLayout(self._labeled_input("Phase [rad]:", self.sawtooth_phase_input))
       self.sawtooth_params.setLayout(sawtooth_layout)

       signal_layout.addWidget(self.sine_button)
       signal_layout.addWidget(self.sine_params)
       signal_layout.addWidget(self.square_button)
       signal_layout.addWidget(self.square_params)
       signal_layout.addWidget(self.sawtooth_button)
       signal_layout.addWidget(self.sawtooth_params)

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

        self.input = self.input_function.input_plot()
        simulation_view.addWidget(self.input)
        simulation_view.addWidget(back_b)
          
#run
if __name__ == "__main__":
    app = QApplication(sys.argv)
    windowapp = Window()
    windowapp.show()
    sys.exit(app.exec_())

     

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
           value = 0.0  
       setattr(self, attr_name, value)
        
    def correct_values(self):
      numerator, denominator = self.get_tf_coefficients()
      correct_num = any(coef != 0 for coef in numerator)
      correct_den = any(coef != 0 for coef in denominator)
      return correct_num and correct_den
    
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
    
    def square_transfer_function(self):
        return square_transfer
    
    def square_input_plot(self):

class InputTriangleFunction:
    def __init__(self, signal_type="triangle"):
        
    def triangle_transfer(self):
        return triagnle_transfer
        
    def triangle_input_plot(self):"""
    
class InputSineFunction:
    def __init__(self, signal_type="sine", amplitude=1.0, frequency=1.0, phase=0.0, duration=10.0, sample_rate=1000):
        self.signal_type = signal_type
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.duration = duration
        self.sample_rate = sample_rate
        self.t = np.linspace(0, duration, int(duration * sample_rate)) #time vecton

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

        #error - input signal
        self.signal_error_label = QLabel("")
        self.signal_error_label.setStyleSheet("color: red")
        self.signal_valid = True 
        self.signal_error_label_added = False
        self.start_menu()

    def update_coefficient(self, line_edit, attr_name):
        value = line_edit.text()
        self.tf_object.update_coefficients(attr_name, value)

    def update_sine(self, line_edit, attr_name):
        value = line_edit.text()
        try:
            self.sine_function.update_sine(attr_name, value)
            self.signal_error_label.setText("")
            self.signal_valid = True

        except ValueError as e:
            self.signal_error_label.setText(str(e))
            self.signal_valid = False
        self.simulate_button.setEnabled(self.signal_valid)


    def update_selected_signal(self):
        if self.sinus_button.isChecked():
            self.selected_signal = "sine"
        elif self.square_button.isChecked():
            self.selected_signal = "square"
        elif self.triangle_button.isChecked():
            self.selected_signal = "triangle"

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
       self.simulate_button.setEnabled(self.signal_valid)
       back_b = QPushButton("Back to start")

       self.simulate_button.clicked.connect(self.simulation)
       back_b.clicked.connect(self.start_menu)

       menu_view.addWidget(QLabel("Numerator of G :"))
       self.numerator_a3_input.setFixedWidth(80)
       self.numerator_a3_input.editingFinished.connect(lambda: self.update_coefficient(self.numerator_a3_input, "a3"))
       a3_layout = QHBoxLayout()
       a3_layout.setAlignment(Qt.AlignLeft)
       a3_layout.addWidget(QLabel("a3:"))
       a3_layout.addWidget(self.numerator_a3_input)
       a3_layout.addStretch()
       menu_view.addLayout(a3_layout)

       self.numerator_a2_input.setFixedWidth(80)
       self.numerator_a2_input.editingFinished.connect(lambda: self.update_coefficient(self.numerator_a2_input, "a2"))
       a2_layout = QHBoxLayout()
       a2_layout.setAlignment(Qt.AlignLeft)
       a2_layout.addWidget(QLabel("a2:"))
       a2_layout.addWidget(self.numerator_a2_input)
       a2_layout.addStretch()
       menu_view.addLayout(a2_layout)

       self.numerator_a1_input.setFixedWidth(80)
       self.numerator_a1_input.editingFinished.connect(lambda: self.update_coefficient(self.numerator_a1_input, "a1"))
       a1_layout = QHBoxLayout()
       a1_layout.setAlignment(Qt.AlignLeft)
       a1_layout.addWidget(QLabel("a1:"))
       a1_layout.addWidget(self.numerator_a1_input)
       a1_layout.addStretch()
       menu_view.addLayout(a1_layout)

       self.numerator_a0_input.setFixedWidth(80)
       self.numerator_a0_input.editingFinished.connect(lambda: self.update_coefficient(self.numerator_a0_input, "a0"))
       a0_layout = QHBoxLayout()
       a0_layout.setAlignment(Qt.AlignLeft)
       a0_layout.addWidget(QLabel("a0:"))
       a0_layout.addWidget(self.numerator_a0_input)
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

       if self.selected_signal == "sine":
            self.sinus_button.setChecked(True)
       elif self.selected_signal == "square":
            self.square_button.setChecked(True)
       elif self.selected_signal == "triangle":
            self.triangle_button.setChecked(True)
       #self.sinus_button.setChecked(True)
       self.sinus_button.toggled.connect(self.update_selected_signal)
       self.square_button.toggled.connect(self.update_selected_signal)
       self.triangle_button.toggled.connect(self.update_selected_signal)

       sine_row_layout = QHBoxLayout()
       self.freq_input = QLineEdit()
       self.freq_input.setFixedWidth(80)
       self.freq_input.setAlignment(Qt.AlignLeft)
       self.freq_input.setText(str(self.sine_function.frequency))
       self.amp_input = QLineEdit()
       self.amp_input.setFixedWidth(80)
       self.amp_input.setAlignment(Qt.AlignLeft)
       self.amp_input.setText(str(self.sine_function.amplitude))
       self.phase_input = QLineEdit()
       self.phase_input.setFixedWidth(80)
       self.phase_input.setAlignment(Qt.AlignLeft)
       self.phase_input.setText(str(self.sine_function.phase))

       freq_layout = QHBoxLayout()
       freq_label = QLabel("Częstotliwość [Hz]:")
       freq_layout.addWidget(freq_label)
       freq_layout.addWidget(self.freq_input)
       freq_layout.addStretch()
       amp_layout = QHBoxLayout()
       amp_label = QLabel("Amplituda [V]:")
       amp_layout.addWidget(amp_label)
       amp_layout.addWidget(self.amp_input)
       amp_layout.addStretch()
       phase_layout = QHBoxLayout()
       phase_label = QLabel("Przesunięcie fazowe [rad]:")
       phase_layout.addWidget(phase_label)
       phase_layout.addWidget(self.phase_input)
       phase_layout.addStretch()
       sine_row_layout.addWidget(self.sinus_button)
       sine_row_layout.addLayout(freq_layout)
       sine_row_layout.addLayout(amp_layout)
       sine_row_layout.addLayout(phase_layout)
       signal_layout.addLayout(sine_row_layout)   
       self.freq_input.editingFinished.connect(lambda: self.update_sine(self.freq_input, "frequency"))
       self.amp_input.editingFinished.connect(lambda: self.update_sine(self.amp_input, "amplitude"))
       self.phase_input.editingFinished.connect(lambda: self.update_sine(self.phase_input, "phase")) 

       signal_layout.addWidget(self.square_button)
       signal_layout.addWidget(self.triangle_button)


       signal_group_box.setLayout(signal_layout)

       menu_view.addWidget(signal_group_box)
       menu_view.addWidget(self.set_parameters_button)
       menu_view.addWidget(self.simulate_button)
       menu_view.addWidget(back_b)


       menu_widget = QWidget()
       menu_widget.setLayout(menu_view)
       self.setCentralWidget(menu_widget)

       menu_view.addWidget(self.signal_error_label)
    
    

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
          
#run
if __name__ == "__main__":
    app = QApplication(sys.argv)
    windowapp = Window()
    windowapp.show()
    sys.exit(app.exec_())

     

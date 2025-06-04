import sympy as sp
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from scipy.signal import sawtooth

class OutputCompute:
    def __init__(self, signal_type, object_info, input_info):
        self.signal_type = signal_type
        self.object_info = object_info
        self.input_info = input_info
        self.num, self.den = self.object_info.get_tf_coefficients()
        self.time_step = 0.01
        self.input_type = self.input_info.signal_type
        self.amplitude = self.input_info.amplitude
        self.frequency = self.input_info.frequency
        self.phase = self.input_info.phase
        self.pulse_width = self.input_info.pulse_width
    
    def get_tf_without_zeros(self):
        def trim_leading_zeros(coeffs):
            for i, c in enumerate(coeffs):
                if c != 0:
                    return coeffs[i:]
            return [0]
        numerator = trim_leading_zeros(self.num)
        denominator = trim_leading_zeros(self.den)
        return numerator, denominator

    def get_system_order(self):
        _, y_coeffs = self.get_tf_without_zeros()
        return len(y_coeffs) - 1

    def rk4_step(self, f, t, x, dt):
        k1 = np.array(f(t, x))
        k2 = np.array(f(t + dt / 2, x + dt / 2 * k1))
        k3 = np.array(f(t + dt / 2, x + dt / 2 * k2))
        k4 = np.array(f(t + dt, x + dt * k3))
        return x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        
    def get_manual_input_derivatives(self, num_derivatives, t, dt):
        derivatives = []
        u_t = self.get_manual_input_value(t)
        derivatives.append(u_t)

        for k in range(1, num_derivatives):
            u_prev = self.get_manual_input_value(t - dt)
            deriv = (derivatives[k-1] - u_prev) / dt
            derivatives.append(deriv)

        return derivatives
    
    def get_manual_input(self, t, num_derivatives):
        dt = self.time_step  # Musisz zdefiniować krok czasowy, np. 0.001
        return self.get_manual_input_derivatives(num_derivatives, t, dt)
    
    def get_manual_input_value(self, t):
        if self.input_type == "sine":
            return self.amplitude * np.sin(2 * np.pi * self.frequency * t + self.phase)
        elif self.input_type == "sawtooth":
            return self.amplitude * sawtooth(2 * np.pi * self.frequency * t + self.phase)
        elif self.input_type == "square":
            temp = self.amplitude * np.sin(2 * np.pi * self.frequency * t + self.phase)
            return self.amplitude * np.where(temp>=0, 1, -1)
        elif self.input_type == "rectangle impulse":
            return self.amplitude * np.where((t>0) & (t<self.pulse_width), 1, 0)
        elif self.input_type == "triangle":
            return self.amplitude * sawtooth(2 * np.pi * self.frequency * t + self.phase, width=0.5 )
    
    def get_f_function(self, t, x):
        u_co, y_co = self.get_tf_without_zeros()
        u_coeffs = list(reversed(u_co))
        y_coeffs = list(reversed(y_co))
        n = self.get_system_order()

        u_vals = self.get_manual_input(t, len(u_coeffs))
        u_vals = u_vals[:len(u_coeffs)]

        left = sum(y_coeffs[i] * x[i] for i in range(n))  # y, y', ..., y^(n-1)
        right = sum(u_coeffs[i] * u_vals[i] for i in range(len(u_coeffs)))  # u, u', ...
        b_n = y_coeffs[n] if n < len(y_coeffs) else 0

        highest_derivative = (right - left) / b_n

        derivatives = np.zeros_like(x)
        derivatives[:-1] = x[1:]
        derivatives[-1] = highest_derivative

        return derivatives

    def simulate_system(self, t_start, t_end, dt):
        n = self.get_system_order()
        x = np.zeros(n)
        t = t_start
        times = []
        outputs = []
        inputs = []

        while t <= t_end:
            times.append(t)
            outputs.append(x[0])
            inputs.append(self.get_manual_input(t, len(self.get_tf_without_zeros()[0]))[0])
            x = self.rk4_step(lambda t_, x_: self.get_f_function(t_, x_), t, x, dt)
            t += dt
        return times, inputs, outputs
        
    def output_plot(self):
        times, inputs, outputs = self.simulate_system(t_start=0.0, t_end=10.0, dt=0.01)
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        ax = self.figure.add_subplot(111)  
        ax.plot(times, outputs)
        ax.set_title("Output signal")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude")
        ax.grid(True)
        self.canvas.draw()
        return self.canvas   

    

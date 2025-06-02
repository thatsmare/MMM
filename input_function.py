import numpy as np
import sympy as sp
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.signal import sawtooth


class InputFunction:
    def __init__(self, signal_type, amplitude=1.0, frequency=1.0, phase=0.0, duration=10.0, sample_rate=1000, pulse_width=1.0):
        self.signal_type = signal_type
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.duration = duration
        self.sample_rate = sample_rate
        self.pulse_width = pulse_width

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
        if attr_name == "pulse width" and value <= 0:
            raise ValueError("Wrong pulse width.")
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
        elif self.signal_type == "square":
            t = np.linspace(0, self.duration, int(self.duration * self.sample_rate), endpoint=False)
            temp = self.amplitude * np.sin(2 * np.pi * self.frequency * t + self.phase)
            y = self.amplitude * np.where(temp>=0, 1, -1)
            return t, y
        elif self.signal_type == "rectangle impulse":
            t = np.linspace(0, self.duration, int(self.duration * self.sample_rate), endpoint=False)
            y = self.amplitude * np.where((t>0) & (t<self.pulse_width), 1, 0)
            return t, y
        elif self.signal_type == "triangle":
            t = np.linspace(0, self.duration, int(self.duration * self.sample_rate), endpoint=False)
            y = self.amplitude * sawtooth(2 * np.pi * self.frequency * t + self.phase, width=0.5 )
            return t, y
        
    def input_symbolic(self):
        t = sp.Symbol('t')
        T = 1/self.frequency

        match self.signal_type:
            case "sine":
                input_symbolic = self.amplitude * sp.sin(2 * sp.pi * self.frequency * t + self.phase)
            case "square":
                input_symbolic = self.amplitude * (sp.Heaviside(t % T) - sp.Heaviside((t % T) - T/2))
            case "sawtooth":
                input_symbolic = self.amplitude * ((t % T) / T - 0.5) * 2
            case "rectangle impulse":
                input_symbolic =  self.amplitude * (sp.Heaviside(t) - sp.Heaviside(t - self.pulse_width))
            case "triangle":
                input_symbolic = sp.Piecewise((4 * self.amplitude / T * (sp.Mod(t,T)) - self.amplitude, (sp.Mod(t,T)) < T / 2),(-4 * self.amplitude / T * (sp.Mod(t,T)) + 3 * self.amplitude, (sp.Mod(t,T)) >= T / 2))
            case _:
                print("Error")
        return input_symbolic

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
        if self.signal_type == "rectangle impulse":
            ax.set_xlim(0, self.pulse_width + 1)
        self.canvas.draw()
        return self.canvas     
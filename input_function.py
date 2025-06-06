import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class InputFunction:
    def __init__(self, signal_type, amplitude=1.0, frequency=1.0, phase=0.0, duration=10.0, pulse_width=1.0, sample_rate=1000):
        self.signal_type = signal_type
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.duration = duration
        self.sample_rate = sample_rate
        self.pulse_width = pulse_width

    def input_generate(self):
        if self.signal_type == "sawtooth":
            t = np.linspace(0, self.duration, int(self.duration * self.sample_rate), endpoint=False)
            T = 1/ self.frequency
            y = (2 * self.amplitude / T) * (t % T) - self.amplitude
            return t, y
        elif self.signal_type == "sine":
            t = np.linspace(0, self.duration, int(self.duration * self.sample_rate), endpoint=False)
            y = self.amplitude * np.sin(2 * np.pi * self.frequency * t + self.phase)
            return t, y
        elif self.signal_type == "square":
            t = np.linspace(0, self.duration, int(self.duration * self.sample_rate), endpoint=False)
            temp=np.sin(2 * np.pi * self.frequency * t + self.phase)
            y = self.amplitude * np.where(temp >= 0, 1, -1)
            return t, y
        elif self.signal_type == "rectangle impulse":
            t = np.linspace(0, self.pulse_width + 1, int(self.duration * self.sample_rate), endpoint=False)
            y = self.amplitude * np.where((t>0) & (t<self.pulse_width), 1, 0)
            return t, y
        elif self.signal_type == "triangle":
            t = np.linspace(0, self.duration, int(self.duration * self.sample_rate), endpoint=False)
            T = 1/ self.frequency
            t_mod = np.mod(t,T)
            y = self.amplitude * (1 - 4 * np.abs(t_mod / T - 0.5))
            return t, y
        elif self.signal_type == "impulse":
            t = np.linspace(0, self.duration, int(self.duration * self.sample_rate), endpoint=False)
            y = np.zeros_like(t)
            idx = np.argmin(np.abs(t - 0.01))
            y[idx] = self.amplitude
            return t, y
        elif self.signal_type == "step":
            t = np.linspace(0, self.duration, int(self.duration * self.sample_rate), endpoint=False)
            y = self.amplitude * np.ones_like(t)
            return t, y

    def input_plot(self):
        t, y = self.input_generate()
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        ax = self.figure.add_subplot(111)  
        ax.plot(t, y)
        ax.set_title(f"Input singal - {self.signal_type}")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("u(t)")
        ax.grid(True)
        self.canvas.draw()
        return self.canvas     

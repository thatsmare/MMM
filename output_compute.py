from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class OutputCompute:
    def __init__(self, signal_type, object_info, input_info):
        self.signal_type = signal_type
        self.object_info = object_info
        self.input_info = input_info
        self.num, self.den = self.object_info.get_tf_coefficients()
        self.a3, self.a2, self.a1, self.a0 = self.num
        self.b4, self.b3, self.b2, self.b1, self.b0 = self.den
        self.dt = 0.01
        self.input_type = self.input_info.signal_type
        self.amplitude = self.input_info.amplitude
        self.frequency = self.input_info.frequency
        self.phase = self.input_info.phase
        self.pulse_width = self.input_info.pulse_width

    def get_manual_input_value(self, t):
        if self.input_type == "sine":
            return self.amplitude * np.sin(2 * np.pi * self.frequency * t + self.phase)
        elif self.input_type == "sawtooth":
            T = 1/ self.frequency
            return (2 * self.amplitude / T) * (t % T) - self.amplitude
        elif self.input_type == "square":
            temp=np.sin(2 * np.pi * self.frequency * t + self.phase)
            return self.amplitude * np.where(temp >= 0, 1, -1)
        elif self.input_type == "rectangle impulse":
            return self.amplitude * np.where((t>0) & (t<self.pulse_width), 1, 0)
        elif self.input_type == "triangle":
            T = 1/ self.frequency
            t_mod = np.mod(t,T)
            return self.amplitude * (1 - 4 * np.abs(t_mod / T - 0.5))
        elif self.input_type == "impulse":
            u = np.zeros_like(t)
            dt = t[1] - t[0]
            idx = np.argmin(np.abs(t - 0.01))
            u[idx] = self.amplitude / dt  # poprawna aproksymacja Diraca
            return u
        elif self.input_type == "step":
            return self.amplitude * np.ones_like(t)
    
    def get_manual_input_derivatives(self, t):
        u = self.get_manual_input_value(t) 
        N = len(t) 
        du1 = np.zeros(N)
        du2 = np.zeros(N)
        du3 = np.zeros(N)
    
        if self.a1 != 0.0 or self.a2 != 0.0 or self.a3 != 0.0:
            for i in range (1,N):
                du1[i] = (u[i] - u[i-1])/self.dt
        if self.a2 != 0.0 or self.a3 != 0.0:
            for i in range (2,N):
                du2[i] = (du1[i] - du1[i-1])/self.dt
        if self.a3 != 0.0:
            for i in range (3,N):
                du3[i] = (du2[i] - du2[i-1])/self.dt
        return u, du1, du2, du3

    def euler_output(self, t):
        u_coeffs = self.num[::-1]    #reverse list
        y_coeffs = self.den[::-1]
        dt = self.dt

        a0, a1, a2, a3, = u_coeffs
        b0, b1, b2, b3, b4 = y_coeffs
        _, n_den = self.object_info.get_system_order()

        u, du1, du2, du3 = self.get_manual_input_derivatives(t)
        N = len(t)
        y = np.zeros(N)
        dy1 = np.zeros(N)
        dy2 = np.zeros(N)
        dy3 = np.zeros(N)
        dy4 = np.zeros(N)

        if n_den == 4:
            for k in range(4, N):
                dy4[k] = (a3*du3[k] + a2*du2[k] + a1*du1[k] + a0*u[k] - b3*dy3[k-1] - b2*dy2[k-1] - b1*dy1[k-1] - b0*y[k-1]) / b4
                dy3[k] = dy3[k-1] + dt * dy4[k]
                dy2[k] = dy2[k-1] + dt * dy3[k]
                dy1[k] = dy1[k-1] + dt * dy2[k]
                y[k] = y[k-1] + dt * dy1[k]
        elif n_den == 3:
            for k in range(3, N):
                dy3[k] = (a3*du3[k] + a2*du2[k] + a1*du1[k] + a0*u[k] - b2*dy2[k-1] - b1*dy1[k-1] - b0*y[k-1]) / b3
                dy2[k] = dy2[k-1] + dt * dy3[k]
                dy1[k] = dy1[k-1] + dt * dy2[k]
                y[k] = y[k-1] + dt * dy1[k]
        elif n_den == 2:
            for k in range(2, N):
                dy2[k] = (a2*du2[k] + a1*du1[k] + a0*u[k] - b1*dy1[k-1] - b0*y[k-1]) / b2
                dy1[k] = dy1[k-1] + dt * dy2[k]
                y[k] = y[k-1] + dt * dy1[k]
        elif n_den == 1:
            for k in range(1, N):
                dy1[k] = (a1*du1[k] + a0*u[k]- b0*y[k-1]) / b1
                y[k] = y[k-1] + dt * dy1[k]
        elif n_den == 0:
            for k in range(N):
                y[k] = a0*u[k] / b0
        return y
        
    def simulate_system(self, t_start, t_end):
        dt=self.dt
        t = np.arange(t_start, t_end + dt, dt) 
        u, _, _, _ = self.get_manual_input_derivatives(t)  
        y = self.euler_output(t)  
        return t, u, y
    
    def output_plot(self):
        times, inputs, outputs = self.simulate_system(0.0, 10.0)
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        ax = self.figure.add_subplot(111)  
        ax.plot(times, outputs, label="y(t)")
        ax.set_title("Output signal")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("y(t)")
        ax.grid(True)
        self.canvas.draw()
        return self.canvas  

    

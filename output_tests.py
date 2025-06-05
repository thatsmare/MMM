import numpy as np
from scipy.signal import square, sawtooth
import matplotlib.pyplot as plt

class TransferFunctionSimulator:
    def __init__(self):
        self.a3, self.a2, self.a1, self.a0 = 0, 0, 3, 1  
        self.b4, self.b3, self.b2, self.b1, self.b0 = 0, 0, 0, 0, 2  
        self.input_type = "square"
        self.amplitude = 2
        self.frequency = 1
        self.phase = 0
        self.pulse_width = 1                         #HERE CHANGE PARAMETERS
        self.dt = 0.01

    def get_tf(self):
        numerator = [self.a3, self.a2, self.a1, self.a0]
        denominator = [self.b4, self.b3, self.b2, self.b1, self.b0]
        return numerator, denominator
    
    def get_system_order(self):
        num, den = self.get_tf()
        def first_nonzero_index(coeffs):
            for i, c in enumerate(coeffs):
                if c != 0:
                    return i
            return len(coeffs)  # all zeros
        num_order = len(num) - first_nonzero_index(num) - 1
        den_order = len(den) - first_nonzero_index(den) - 1
        return num_order, den_order
    
    def get_manual_input_value(self, t):
        if self.input_type == "sine":
            return self.amplitude * np.sin(2 * np.pi * self.frequency * t + self.phase)
        elif self.input_type == "sawtooth":
            return self.amplitude * sawtooth(2 * np.pi * self.frequency * t + self.phase)
        elif self.input_type == "square":
            return self.amplitude * square(2 * np.pi * self.frequency * t + self.phase)
        elif self.input_type == "rectangle impulse":
            return self.amplitude * np.where((t>0) & (t<self.pulse_width), 1, 0)
        elif self.input_type == "triangle":
            return self.amplitude * sawtooth(2 * np.pi * self.frequency * t + self.phase, width=0.5)
        elif self.input_type == "impulse":
            u = np.zeros_like(t)
            idx = np.argmin(np.abs(t - 0.01))
            u[idx] = self.amplitude
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
        u_co, y_co = self.get_tf()
        u_coeffs = u_co[::-1]    #reverse list
        y_coeffs = y_co[::-1]
        dt = self.dt

        a0, a1, a2, a3, = u_coeffs
        b0, b1, b2, b3, b4 = y_coeffs
        _, n_den = self.get_system_order()

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
        plt.figure(figsize=(10, 5))

        plt.subplot(2, 1, 1)
        plt.plot(times, inputs, label="u(t) - Wejście")
        plt.ylabel("u(t)")
        plt.title("Wejście i wyjście układu")
        plt.grid(True)
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(times, outputs, label="y(t) - RK4")
        plt.xlabel("Czas [s]")
        plt.ylabel("y(t)")
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.show()

sim = TransferFunctionSimulator()
sim.output_plot()



"""def get_manual_triangle_derivatives(self, num_derivatives):
        t = sp.Symbol('t')
        T = 1 / self.frequency
        A = self.amplitude
        mod = sp.Mod(t, T)
        expr = sp.Piecewise((4 * A / T * mod - A, mod < T / 2),(-4 * A / T * mod + 3 * A, mod >= T / 2))
        derivatives = [expr]
        for _ in range(1, num_derivatives):
            expr = sp.diff(expr, t)
            derivatives.append(expr)
        return [lambdify(t, d, 'numpy') for d in derivatives]

    def get_manual_rectangle_impulse_derivatives(self, num_derivatives):
        t = sp.Symbol('t')
        input_symbolic = sp.Piecewise((self.amplitude, (t >= 0) & (t < self.pulse_width)),(0, True))
        derivatives = [input_symbolic]
        for _ in range(1, num_derivatives):
            input_symbolic = sp.diff(input_symbolic, t)
            derivatives.append(input_symbolic)
        return [lambdify(t, d, 'numpy') for d in derivatives]

    def get_manual_sawtooth_derivatives(self, num_derivatives):
        t = sp.Symbol('t')
        T = 1 / self.frequency
        expr = self.amplitude * ((sp.Mod(t, T)) / T - 0.5) * 2
        derivatives = [expr]
        for _ in range(1, num_derivatives):
            expr = sp.diff(expr, t)
            derivatives.append(expr)
        return [lambdify(t, d, 'numpy') for d in derivatives]

    def get_manual_square_derivatives(self, num_derivatives):
        t = sp.Symbol('t')
        T = 1 / self.frequency
        expr = sp.Piecewise((self.amplitude, sp.Mod(t, T) < T / 2),(-self.amplitude, True))
        derivatives = [expr]
        for _ in range(1, num_derivatives):
            expr = sp.diff(expr, t)
            derivatives.append(expr)
        return [lambdify(t, d, 'numpy') for d in derivatives]

    def get_manual_sine_derivatives(self, num_derivatives):
        t = sp.Symbol('t')
        ω = 2 * sp.pi * self.frequency
        expr = self.amplitude * sp.sin(ω * t + self.phase)
        derivatives = [expr]
        for _ in range(1, num_derivatives):
            expr = sp.diff(expr, t)
            derivatives.append(expr)
        return [lambdify(t, d, 'numpy') for d in derivatives]
    
    def get_manual_input(self, t, num_derivatives):
        if self.input_type == "sine":
            derivatives = self.get_manual_sine_derivatives(num_derivatives)
        elif self.input_type == "square":
            derivatives = self.get_manual_square_derivatives(num_derivatives)
        elif self.input_type == "sawtooth":
            derivatives = self.get_manual_sawtooth_derivatives(num_derivatives)
        elif self.input_type == "rectangle impulse":
            derivatives = self.get_manual_rectangle_impulse_derivatives(num_derivatives)
        elif self.input_type == "triangle":
            derivatives = self.get_manual_triangle_derivatives(num_derivatives)
        else:
            raise ValueError(f"Unsupported input_type: {self.input_type}")
        return self.input_derivatives(t, derivatives)
    
    def input_derivatives(self, t_val, derivatives):
        return [f(t_val) for f in derivatives]"""
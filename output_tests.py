import numpy as np
from scipy.signal import TransferFunction, lsim
from scipy.signal import square, sawtooth
import matplotlib.pyplot as plt
import sympy as sp
from sympy import lambdify

class TransferFunctionSimulator:
    def __init__(self):
        self.a3, self.a2, self.a1, self.a0 = 0, 0, 2, 3  # współczynniki licznika
        self.b4, self.b3, self.b2, self.b1, self.b0 = 0, 0, 2, 2, 1  # współczynniki mianownika
        self.input_type = "triangle"
        self.amplitude = 1
        self.frequency = 1
        self.phase = 0
        self.pulse_width = 1                         #HERE CHANGE PARAMETERS
        self.time_step = 0.01

    def get_tf_without_zeros(self):
        def trim_leading_zeros(coeffs):
            for i, c in enumerate(coeffs):
                if c != 0:
                    return coeffs[i:]
            return [0]
        numerator = trim_leading_zeros([self.a3, self.a2, self.a1, self.a0])
        denominator = trim_leading_zeros([self.b4, self.b3, self.b2, self.b1, self.b0])
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
        

# -----------------------------MANUAL DERIVATIVES FOR EACH TYPE OF INPUT-------------------------------------------
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
        return [lambdify(t, d, 'numpy') for d in derivatives]"""
    
    """def get_manual_input(self, t, num_derivatives):
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
        return self.input_derivatives(t, derivatives)"""
    
    """def input_derivatives(self, t_val, derivatives):
        return [f(t_val) for f in derivatives]"""
    
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

#---------------------------------------------------------------------------------------------------------------------

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
        times, inputs, outputs = self.simulate_system(0.0, 10.0, 0.01)
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


# Uruchomienie
sim = TransferFunctionSimulator()
sim.output_plot()
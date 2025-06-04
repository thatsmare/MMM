import sympy as sp
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class OutputCompute:
    def __init__(self, signal_type, object_info, input_info):
        self.signal_type = signal_type
        self.object_info = object_info
        self.input_info = input_info
    
    def rk4_step(self, f, t, x, dt):
        k1 = np.array(f(t, x))
        k2 = np.array(f(t + dt/2, x + dt/2 * k1))
        k3 = np.array(f(t + dt/2, x + dt/2 * k2))
        k4 = np.array(f(t + dt,   x + dt * k3))
        return x + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
            
    def get_system_order(self):
        _, y_coeffs = self.get_tf_without_zeros()
        return len(y_coeffs) - 1

    def get_tf_without_zeros(self):
        num, den = self.object_info.get_tf_coefficients()
        def trim_leading_zeros(coeffs):
            for i, c in enumerate(coeffs):
                if c != 0:
                    return coeffs[i:]
            return [0]
        numerator = trim_leading_zeros(num)
        denominator = trim_leading_zeros(den)
        return numerator, denominator
    
    def update_input_reference(self, new_input_info):
        self.input_info = new_input_info
        
    def get_manual_input(self, t):
        return self.input_info.input_derivatives(t, self.input_info.get_manual_sine_derivatives())

    def get_f_function(self, t, x):
        u_co, y_co = self.get_tf_without_zeros()
        u_coeffs = list(reversed(u_co))  
        y_coeffs = list(reversed(y_co))
        n = self.get_system_order()

        u_vals = self.get_manual_input(t)
        u_vals = u_vals[:len(u_coeffs)]
        # y⁽ⁿ⁾ = (a0*u + a1*u' + ... - b0*y - b1*y' - ...)/bn
        left = sum(y_coeffs[i] * x[i] for i in range(n))  # y, y', ..., y⁽ⁿ⁻¹⁾
        right = sum(u_coeffs[i] * u_vals[i] for i in range(min(len(u_coeffs), len(u_vals))))  # u, u', ...
        b_n = y_coeffs[n] if n < len(y_coeffs) else 0
        highest_derivative = (right - left) / b_n

        derivatives = np.zeros_like(x)
        derivatives[:-1] = x[1:]
        derivatives[-1] = highest_derivative 
        return derivatives
    
    def simulate_system(self, t_start, t_end, dt):
        # Initialize x
        n = self.get_system_order()
        x = np.zeros(n)
        t = t_start
        times = []
        outputs = []
        inputs = []

        # RK4 
        while t <= t_end:
            times.append(t)
            outputs.append(x[0])  
            inputs.append(self.get_manual_input(t)[0])
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

    def get_differential_equation(self):
        # symbols needed, y,y1,.../u,u1,... next derivatives(pochodne)
        self.y_diff = [
            sp.Symbol('y'),
            sp.Symbol('y1'),
            sp.Symbol('y2'),
            sp.Symbol('y3'),
            sp.Symbol('y4'),
            ]
        self.u_diff = [
            sp.Symbol('u'),
            sp.Symbol('u1'),
            sp.Symbol('u2'),
            sp.Symbol('u3'),
            ]
                
        numerator, denominator = self.object_info.get_tf_coefficients()
        
        # left side of the equation - all y(t)
        y_side = sum(coefficient *self.y_diff[i]  for i, coefficient in enumerate(reversed(denominator)))
        
        #Right side of the equation - all u(t)
        u_side = sum(coefficient *self.u_diff[i]  for i, coefficient in enumerate(reversed(numerator)))        
        
        differential_equation = sp.Eq(y_side, u_side)
        print(y_side)
        print(u_side)
        
        return differential_equation 
    
    def get_output(self, diff_equation):
        #self.y_diff, self_u_diff #symbols 
        u = self.input_info.input_symbolic #SYMBOLIC t
        u1 = 1   #diff_function(u,t)
        u2 = 2   #diff_function(u1,t)
        u3 = 3   #diff_function(u2,t)
        u_symbolic = [u, u1, u2, u3]
        
        diff_equation = diff_equation.subs(self.u_diff, u_symbolic)

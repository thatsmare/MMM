import sympy as sp
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class OutputCompute:
    def __init__(self, signal_type, object_info, input_info):
        self.signal_type = signal_type
        self.object_info = object_info
        self.input_info = input_info
        input_info.prepare_input_derivatives()
      
    def rk4_step(self, f, t, x, dt):
        k1 = np.array(f(t, x))
        k2 = np.array(f(t + dt/2, x + dt/2 * k1))
        k3 = np.array(f(t + dt/2, x + dt/2 * k2))
        k4 = np.array(f(t + dt,   x + dt * k3))
        return x + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
    
    def get_system_order(self):
        _, y_coeffs = self.object_info.get_tf_coefficients()
        #Order - the higher y index
        n = max((i for i, b in enumerate(y_coeffs) if b != 0), default=0)
        return n

    def get_f_function(self, t, x):
        u_co, y_co = self.object_info.get_tf_coefficients()
        u_coeffs = list(u_co)  
        y_coeffs = list(y_co)

        n = self.get_system_order()

        # u derivatives u(t), u'(t), ...
        u_vals = self.input_info.input_derivatives(t)

        # y⁽ⁿ⁾ = (a₀*u + a₁*u' + ... - b₀*y - b₁*y' - ...)/bₙ
        left = sum(y_coeffs[i] * x[i] for i in range(n))  # y, y', ..., y⁽ⁿ⁻¹⁾
        right = sum(a * u_vals[i] for i, a in enumerate(u_coeffs) if i < len(u_vals))  # u, u', ..., u⁽ᵐ⁾
        b_n = y_coeffs[n] if n < len(y_coeffs) else 0
        highest_derivative = (right - left) / b_n

        derivatives = list(x[1:n+1])
        derivatives.append(highest_derivative)  
        #print(derivatives)
        return derivatives
    
    def simulate_system(self, t_start, t_end, dt):
        # Initialize x
        n = self.get_system_order()
        x = np.zeros(n + 1)
        t = t_start
        times = []
        outputs = []

        # RK4 
        while t <= t_end:
            times.append(t)
            outputs.append(x[0])  

            f = lambda t_val, x_val: self.get_f_function(t_val, x_val)

            x = self.rk4_step(f, t, x, dt)
            t += dt
        return times, outputs
            
        
    def output_plot(self):
        times, outputs = self.simulate_system(t_start=0.0, t_end=5.0, dt=0.01)
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

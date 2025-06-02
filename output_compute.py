import sympy as sp
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class OutputCompute:
    def __init__(self, signal_type, object_info, input_info):
        self.signal_type = signal_type
        self.object_info = object_info
        self.input_info = input_info
      
    """def differentation_rk4(self, t_max=10.0, dt=0.01):
        # Ustawienie osi czasu
        self.t = np.arange(0, t_max, dt)
        n = len(self.t)
        
        # Pobierz transmitancję jako współczynniki licznika i mianownika
        numerator, denominator = self.tf_object.get_tf_coefficients()
        
        # Sprawdź rząd układu (liczba równa rzędom pochodnych y)
        order = len(denominator) - 1

        # Znormalizuj współczynniki, aby najwyższy współczynnik mianownika był 1
        denominator = [d / denominator[0] for d in denominator]
        numerator = [n / denominator[0] for n in numerator]

        # Zdefiniuj funkcję wejściową u(t) (tutaj: sinusoidalna jako przykład)
        u = np.array([self.input_function.evaluate_numeric(ti) for ti in self.t])

        # Przygotuj wektor stanu y = [y, y', y'', ...]
        y = np.zeros((n, order))
        
        # Definiujemy układ równań pierwszego rzędu
        def state_derivative(ti, yi, ui):
            # yi: aktualny wektor stanu [y, y', y'', ...]
            derivatives = np.zeros(order)
            for i in range(order - 1):
                derivatives[i] = yi[i+1]

            # Oblicz najwyższą pochodną z równania różniczkowego
            # y^(n) = -a1*y^(n-1) - a2*y^(n-2) ... + b0*u + b1*u' ...
            y_terms = sum(-denominator[i+1] * yi[i] for i in range(order - 1))
            u_terms = 0
            for j in range(len(numerator)):
                if j == 0:
                    u_terms += numerator[-1] * ui
                elif ti - j*dt >= 0:
                    u_terms += numerator[-(j+1)] * self.input_function.evaluate_numeric(ti - j*dt)
            derivatives[-1] = y_terms + u_terms
            return derivatives

        # RK4 iteracja
        for i in range(n - 1):
            ti = self.t[i]
            yi = y[i]
            ui = u[i]

            k1 = dt * state_derivative(ti, yi, ui)
            k2 = dt * state_derivative(ti + dt/2, yi + k1/2, u[i])
            k3 = dt * state_derivative(ti + dt/2, yi + k2/2, u[i])
            k4 = dt * state_derivative(ti + dt, yi + k3, u[i])

            y[i+1] = yi + (k1 + 2*k2 + 2*k3 + k4) / 6

        # Przypisz wynik do y do wykresu
        self.y = y[:, 0]
        return self.y"""
        
    def output_plot(self):
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        ax = self.figure.add_subplot(111)  
        ax.plot(self.t, self.y)
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
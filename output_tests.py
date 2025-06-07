import numpy as np
import matplotlib.pyplot as plt

class TransferFunctionSimulator:
    def __init__(self):
        self.a3, self.a2, self.a1, self.a0 = 0, 0, 0, 1  
        self.b4, self.b3, self.b2, self.b1, self.b0 = 0, 0, 4, 3, 2  
        self.input_type = "impulse"
        self.amplitude = 2
        self.frequency = 1
        self.phase = 0
        self.pulse_width = 1                         #HERE CHANGE PARAMETERS
        self.dt = 0.001

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
            if isinstance(t, np.ndarray):
                return self.amplitude * ((np.abs(t - 0.01) < self.dt / 2).astype(float))
            else:
                return self.amplitude if abs(t - 0.01) < self.dt / 2 else 0
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
    
    #--------------------------------------------------------------------------
    
    def rk4_step(self, f, t, x):
        dt = self.dt 
        k1 = np.array(f(t, x))
        k2 = np.array(f(t + dt / 2, x + dt / 2 * k1))
        k3 = np.array(f(t + dt / 2, x + dt / 2 * k2))
        k4 = np.array(f(t + dt, x + dt * k3))
        return x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    
    def get_manual_input_derivatives_at(self, t):
        dt = self.dt
        u = self.get_manual_input_value(t)
        u1 = self.get_manual_input_value(t - dt)
        u2 = self.get_manual_input_value(t - 2 * dt)
        u3 = self.get_manual_input_value(t - 3 * dt)

        du1 = (u - u1) / dt
        du2 = (u - 2 * u1 + u2) / dt**2
        du3 = (u - 3 * u1 + 3 * u2 - u3) / dt**3
        return u, du1, du2, du3

    def get_f_function(self, t, x):
        u_co, y_co = self.get_tf()
        u_coeffs = u_co[::-1]    #reverse list
        y_coeffs = y_co[::-1]

        a0, a1, a2, a3, = u_coeffs
        b0, b1, b2, b3, b4 = y_coeffs
        _, n_den = self.get_system_order()

        u, du1, du2, du3 = self.get_manual_input_derivatives_at(t)
        dy = 0

        if n_den == 4:
            dy = (a3 * du3 + a2 * du2 + a1 * du1 + a0 * u
                  - b3 * x[3] - b2 * x[2] - b1 * x[1] - b0 * x[0]) / b4
        elif n_den == 3:
            dy = (a3 * du3 + a2 * du2 + a1 * du1 + a0 * u
                  - b2 * x[2] - b1 * x[1] - b0 * x[0]) / b3
        elif n_den == 2:
            dy = (a2 * du2 + a1 * du1 + a0 * u
                  - b1 * x[1] - b0 * x[0]) / b2
        elif n_den == 1:
            dy = (a1 * du1 + a0 * u - b0 * x[0]) / b1
        elif n_den == 0:
            dy = a0 * u / b0

        derivatives = np.zeros_like(x)
        for j in range(n_den - 1):
            derivatives[j] = x[j + 1]
        derivatives[n_den - 1] = dy
        return derivatives
        
    def simulate_rk(self, t_start, t_end):
        dt=self.dt
        _, n = self.get_system_order()
        x = np.zeros(n)
        t = t_start
        times = []
        outputs = []
        inputs = []

        while t <= t_end:
            times.append(t)
            outputs.append(x[0])
            inputs.append(self.get_manual_input_value(t))
            x = self.rk4_step(lambda t_, x_: self.get_f_function(t_, x_), t, x)
            t += dt
        return np.array(times), np.array(inputs), np.array(outputs)
    


    #------------------------------------------------------------------------------------------------
        
    def simulate_system(self, t_start, t_end):
        dt=self.dt
        t = np.arange(t_start, t_end + dt, dt) 
        u = self.get_manual_input_value(t)  
        y = self.euler_output(t)  
        return t, u, y
    
    def output_plot(self):
        times, inputs, outputs = self.simulate_system(0.0, 10.0)
        times1, inputs1, outputs1 = self.simulate_rk(0.0, 10.0)
        plt.figure(figsize=(10, 5))

        plt.subplot(2, 1, 1)
        plt.plot(times, inputs, label="u(t) - Wejście")
        plt.ylabel("u(t)")
        plt.title("Wejście i wyjście układu")
        plt.grid(True)
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(times, outputs, label="y(t) - euler")
        plt.plot(times1, outputs1, label="y(t) - RK4", linestyle="--")
        plt.xlabel("Czas [s]")
        plt.ylabel("y(t)")
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.show()

sim = TransferFunctionSimulator()
sim.output_plot()




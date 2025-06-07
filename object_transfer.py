from scipy.signal import TransferFunction
import sympy as sp
import matplotlib.pyplot as plt

class ObjectTransfer:
    def __init__(self):
      self.b4 = 0.0
      self.b3 = 0.0
      self.b2 = 1.0
      self.b1 = 1.0
      self.b0 = 1.0
      self.a3 = 0.0
      self.a2 = 0.0
      self.a1 = 1.0
      self.a0 = 1.0

    def get_tf_coefficients(self):
      numerator = [self.a3, self.a2, self.a1, self.a0]
      denominator = [self.b4, self.b3, self.b2, self.b1, self.b0]
      return numerator, denominator
    
    def get_system_order(self):
        num, den = self.get_tf_coefficients()
        def first_nonzero_index(coeffs):
            for i, c in enumerate(coeffs):
                if c != 0:
                    return i
            return len(coeffs)  # all zeros
        num_order = len(num) - first_nonzero_index(num) - 1
        den_order = len(den) - first_nonzero_index(den) - 1
        return num_order, den_order
    
    def get_tf(self):
        num, den = self.get_tf_coefficients()
        return TransferFunction(num, den)
    
    def zeros_and_poles(self):
        tf = self.get_tf()
        return list(tf.zeros), list(tf.poles)
    
    def get_symbolic_tf(self):
        s = sp.Symbol('s')
        symbolic_tf = (self.a0 + self.a1*s + self.a2*s**2 + self.a3 * s**3)/(self.b0 + self.b1*s + self.b2*s**2 + self.b3*s**3 + self.b4*s**4)
        return symbolic_tf
    
    def plot_zeros_poles(self):
        zeros, poles = self.zeros_and_poles()
        plt.close('all') 

        fig = plt.figure(figsize=(8, 8))  
        mgr = plt.get_current_fig_manager()
        try:
            mgr.window.move(1900, 200)
        except Exception as e:
            print(f"Nie udało się ustawić pozycji okna: {e}")

        if zeros:
            plt.plot([z.real for z in zeros], [z.imag for z in zeros], 'go', label='Zeros')     
        if poles:
            plt.plot([p.real for p in poles], [p.imag for p in poles], 'rx', label='Poles')  
        plt.axhline(0, color='black', lw=0.5)
        plt.axvline(0, color='black', lw=0.5)
        plt.grid(True)
        plt.xlabel('Real part')
        plt.ylabel('Imaginary part')
        plt.title('Zeros and poles')
        plt.legend()
        plt.axis('equal')
        plt.show()
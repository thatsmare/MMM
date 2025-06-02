from scipy.signal import TransferFunction
import sympy as sp

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
    
    def update_coefficients(self, attr_name, value):
       try:
            value = float(value)
       except ValueError:
            raise ValueError(f"{attr_name.capitalize()} was not a number.")
       setattr(self, attr_name, value)
        
    def correct_values(self):
      numerator, denominator = self.get_tf_coefficients()
      all_floats = all(isinstance(c, float) for c in numerator + denominator)
      correct_num = any(coef != 0 for coef in numerator)
      correct_den = any(coef != 0 for coef in denominator)
      return correct_num and correct_den and all_floats
    
    def get_tf(self):
        if not self.correct_values():
            raise ValueError("Incorrect transfer function")
        num, den = self.get_tf_coefficients()
        return TransferFunction(num, den)
    
    def zeros_and_poles(self):
        tf = self.get_tf()
        return list(tf.zeros), list(tf.poles)
    
    def get_symbolic_tf(self):
        s = sp.Symbol('s')
        symbolic_tf = (self.a0 + self.a1*s + self.a2*s**2 + self.a3 * s**3)/(self.b0 + self.b1*s + self.b2*s**2 + self.b3*s**3 + self.b4*s**4)
        return symbolic_tf
import sympy as sp
import numpy as np

def get_input_in_t(signal_type):
        s, A, f, phase, pulse_width = sp.symbols('s A f phase pulse_width')
        T = 1/f

        match signal_type:
            case "sine":
                input_laplace = (A*(s*sp.sin(phase) + 2*np.pi*f*sp.cos(phase))/(s**2 + (2*np.pi*f)**2)) #sp for symbolic
            case "square":
                input_laplace = (A/s)*((1-sp.exp(-s*0.5*T))/(1 - sp.exp(-s*T)))
            case "sawtooth":
                input_laplace = (1/(1-sp.exp(-s*T))) * (A/T)* ((1-sp.exp(-s*T))*(1 + s*T)/s**2)
            case "rectangle impulse":
                input_laplace =  A/s * (1 - sp.exp(-s*pulse_width))
            case "triangle":
                input_laplace = A/s**2 * (1 - sp.exp(-s*T) * (s*T + 1) + sp.exp(-2*s*T) * (s*T - 1))
            case _:
                print("Error, could not get Laplace of input signal")
        return input_laplace
    
def laplace_output(Linput, tf_object):
        return Linput*tf_object
    
     # Inverse -> derivative -> plot
def inverse_Laplace(laplace_expr):
        s, t = sp.symbols('s t')
        return sp.inverse_laplace_transform(laplace_expr, s, t) 
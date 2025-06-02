import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.signal import freqs

class BodePlot:
    def __init__(self, tf_object):
      self.tf_object = tf_object
      self.numerator, self.denominator = self.tf_object.get_tf_coefficients()
      zeros, poles = self.tf_object.zeros_and_poles()

      #Zero is bad at log scale
      zeros_and_poles = [abs(f) for f in zeros + poles if abs(f) > 1e-6]

     # preparing range of the plot
      if zeros_and_poles:
        min_value = 0.1 * min(zeros_and_poles)
        max_value = 10 * max(zeros_and_poles)
      else:
        min_value = 0.1
        max_value = 100
      
      #the necessary range of the plot
      self.range = [min_value, max_value]
      self.figure = Figure(figsize=(6, 4))
      self.canvas = FigureCanvas(self.figure)
      self.plotting_bode()
    
    def plotting_bode(self):
        ax_mag = self.figure.add_subplot(211)
        ax_ph = self.figure.add_subplot(212, sharex=ax_mag) #rows,col,index
        
        # w to put in tf
        w = np.logspace(np.log10(self.range[0]), np.log10(self.range[1]), 1000) # 1000 points to count
        
        # counts tf(j*w)
        w, plot_line = freqs(self.numerator, self.denominator,w)

        #change to dB and angle respectively
        magnitude = 20 * np.log10(abs(plot_line))
        phase = np.angle(plot_line, deg=True)
        
        # --- Zapas wzmocnienia (gain margin) ---
        gain_margin = None
        gain_margin_freq = None
        for i in range(len(phase) - 1):
            if (phase[i] + 180) * (phase[i + 1] + 180) < 0:
                # Interpolacja liniowa częstotliwości
                w1, w2 = w[i], w[i + 1]
                p1, p2 = phase[i], phase[i + 1]
                m1, m2 = magnitude[i], magnitude[i + 1]
                w_cross = w1 + (w2 - w1) * (-180 - p1) / (p2 - p1)
                mag_cross = m1 + (m2 - m1) * (w_cross - w1) / (w2 - w1)
                if mag_cross < 0:
                    gain_margin = -mag_cross
                    gain_margin_freq = w_cross
                break  # bierzemy pierwsze przecięcie

        # --- Zapas fazy (phase margin) ---
        phase_margin = None
        phase_margin_freq = None
        for i in range(len(magnitude) - 1):
            if magnitude[i] * magnitude[i + 1] < 0:
                w1, w2 = w[i], w[i + 1]
                m1, m2 = magnitude[i], magnitude[i + 1]
                p1, p2 = phase[i], phase[i + 1]
                w_cross = w1 + (w2 - w1) * (0 - m1) / (m2 - m1)
                phase_cross = p1 + (p2 - p1) * (w_cross - w1) / (w2 - w1)
                phase_margin = 180 + phase_cross
                phase_margin_freq = w_cross
                break

        # --- Ocena stabilności ---
        self.gain_margin = gain_margin
        self.phase_margin = phase_margin
        self.stable = (gain_margin is not None and gain_margin > 0 and phase_margin is not None and phase_margin > 0)

        """#STABILITY
        to_zero = np.abs(phase + 180) #we're looking for phase at -180 so minimazing it to 0
        phase_180_idx = np.argmin(to_zero)
        magnitude_180 = magnitude[phase_180_idx]
        gain_margin = -magnitude_180 #zapas wzmocnienia

        gain_0_idx = np.argmin(np.abs(magnitude))
        phase_0 = phase[gain_0_idx]
        phase_margin = 180 + phase_0   

        if gain_margin and phase_margin > 0:
            self.stable = True
        else:
            self.stable = False"""

        #Plotting magnitude
        ax_mag.set_title("Magnitude Bode Plot")
        ax_mag.set_xlabel("Frequency [rad/s]")
        ax_mag.set_ylabel("Magnitude [dB]")
        ax_mag.set_xscale("log") # log on x axis
        ax_mag.plot(w, magnitude)

        #PLotting phase
        ax_ph.set_title("Phase Bode Plot")
        ax_ph.set_xlabel("Frequency [rad/s]")
        ax_ph.set_ylabel("Phase [°]")
        ax_ph.set_xscale("log") # log on x axis
        ax_ph.plot(w, phase)

        # Linie pomocnicze na wykresie amplitudy i fazy
        ax_mag.axhline(0, color='grey', linestyle='--')
        ax_ph.axhline(-180, color='grey', linestyle='--')
        if gain_margin_freq:
            ax_mag.axvline(gain_margin_freq, color='red', linestyle='--', label="Gain Margin")
            ax_mag.legend()
        if phase_margin_freq:
            ax_ph.axvline(phase_margin_freq, color='red', linestyle='--', label="Phase Margin")
            ax_ph.legend()
         
        self.canvas.draw()
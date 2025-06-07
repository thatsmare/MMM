import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.signal import freqs

class BodePlot:
    def __init__(self, tf_object):
      self.tf_object = tf_object
      self.numerator, self.denominator = self.tf_object.get_tf_coefficients()
      zeros, poles = self.tf_object.zeros_and_poles()
      
      negative_poles = all(np.real(p) <= 0 for p in poles)
      
      if not negative_poles:
          self.correct_phase = True
      else:
          self.correct_phase = False

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
        
        phase =np.unwrap(np.angle(plot_line, deg=True))
        if self.correct_phase: phase -= 360
        
        #STABILITY
        zeros, poles = self.tf_object.zeros_and_poles()
        
        
        stable_poles = all(np.real(p) <= 0 for p in poles)
        
        if not stable_poles:
            self.stable = False
        else:
            to_zero = np.abs(phase + 180) #we're looking for phase at -180 so minimazing it to 0
            gain_margin_freq = np.argmin(to_zero)
            if to_zero[gain_margin_freq] < 2: 
                gain_margin = -magnitude[gain_margin_freq]
            else:
                gain_margin = np.inf    #inf when the phase doesn't dip below 180

            phase_margin_freq  = np.argmin(np.abs(magnitude))
            phase_0 = phase[phase_margin_freq]
            phase_margin = 180 + phase_0 
                        
            if gain_margin > 0 and phase_margin > 0:
                self.stable = True
            else:
                self.stable = False           

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

        if stable_poles:
            ax_mag.axvline(w[gain_margin_freq], color='red', linestyle='--', 
                        label=f"Gain Margin: {gain_margin:.1f} dB")
            ax_ph.axvline(w[phase_margin_freq], color='blue', linestyle='--', 
                        label=f"Phase Margin: {phase_margin:.1f}°")
            ax_mag.legend()
            ax_ph.legend()
            
        self.canvas.draw()
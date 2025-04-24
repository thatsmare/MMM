"""""
MMM project exercise number 10

Made by Martyna Penkowska 197926 and Natalia Sampławska 197573

"""""

import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QHBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sine Wave Plotter")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Input controls
        controls_layout = QHBoxLayout()
        self.freq_input = QLineEdit("1.0")
        self.freq_input.setPlaceholderText("Frequency (Hz)")
        plot_button = QPushButton("Plot")
        plot_button.clicked.connect(self.plot_signal)
        controls_layout.addWidget(QLabel("Frequency (Hz):"))
        controls_layout.addWidget(self.freq_input)
        controls_layout.addWidget(plot_button)
        main_layout.addLayout(controls_layout)

        # Plotting area
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # Initial plot
        self.plot_signal()

    def plot_signal(self):
        try:
            freq = float(self.freq_input.text())
        except ValueError:
            freq = 1.0

        x = np.linspace(0, 2, 1000)
        y = np.sin(2 * np.pi * freq * x)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        ax.set_title(f"Sine Wave (f = {freq:.2f} Hz)")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        self.canvas.draw()

# Run app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotWindow()
    window.show()
    sys.exit(app.exec_())


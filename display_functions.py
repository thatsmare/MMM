from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit,
    QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QRadioButton, QGroupBox
)
from PyQt5.QtCore import Qt


class DisplayFunctions:
    def __init__(self, signal_type, tf_object, input_function):
        self.signal_type = signal_type
        self.tf_object = tf_object
        self.input_function = input_function
        self.transfer_valid = True
        self.signal_valid = True


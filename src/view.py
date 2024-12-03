import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np

class AudioView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Audio Analysis Tool")
        self.current_band_index = 0  # Initialize current_band_index
        self.create_widgets()



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
    def create_widgets(self):
        self.load_button = tk.Button(self.root, text="Load Audio File", command=self.controller.load_audio_file)
        self.load_button.pack(pady=10)

        self.file_label = tk.Label(self.root, text="No file loaded", wraplength=400)
        self.file_label.pack(pady=10)
        self.duration_label = tk.Label(self.root, text="Audio Duration: N/A", wraplength=400)
        self.duration_label.pack(pady=10)

        self.results_label = tk.Label(self.root, text="", wraplength=400)
        self.results_label.pack(pady=10)

        self.waveform_button = tk.Button(self.root, text="Show Waveform", command=self.controller.display_waveform, state=tk.DISABLED)
        self.waveform_button.pack(pady=10)

        self.rt60_button = tk.Button(self.root, text="Compute RT60", command=self.controller.compute_rt60, state=tk.DISABLED)
        self.rt60_button.pack(pady=10)

        self.alternate_rt60_button = tk.Button(self.root, text="Alternate RT60 Plots", command=self.controller.alternate_rt60_plots, state=tk.DISABLED)
        self.alternate_rt60_button.pack(pady=10)

        self.resonance_button = tk.Button(self.root, text="Show Highest Resonance", command=self.controller.show_highest_resonance, state=tk.DISABLED)
        self.resonance_button.pack(pady=10)

        self.combine_rt60_button = tk.Button(self.root, text="Combine RT60 Plots", command=self.controller.combine_rt60_plots, state=tk.DISABLED)
        self.combine_rt60_button.pack(pady=10)

        self.rt60_difference_button = tk.Button(self.root, text="RT60 Difference", command=self.controller.show_rt60_difference, state=tk.DISABLED)
        self.rt60_difference_button.pack(pady=10)


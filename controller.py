from model import AudioModel
from view import AudioView
import matplotlib.pyplot as plt
import numpy as np


class AudioController:
    def __init__(self):
        self.model = AudioModel()
        self.view = AudioView(self)

    def load_audio_file(self):
        from tkinter import filedialog  # Import filedialog here for use
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.m4a")])  # Open file dialog
        if file_path:  # Check if a file was selected
            try:
                result = self.model.load_audio(file_path)
                duration = self.model.compute_audio_duration()
                self.view.update_status(self.view.file_label, f"Loaded: {file_path}")
                self.view.update_status(self.view.duration_label, f"Audio Duration: {duration:.2f} seconds")
                self.view.update_status(self.view.results_label, result)
                self.view.enable_buttons()
            except Exception as e:
                self.view.update_status(self.view.results_label, f"Error: {e}")
        else:
            self.view.update_status(self.view.results_label, "Error: No file selected.")

    def display_waveform(self):
        try:
            audio_data, sample_rate = self.model.get_waveform()
            time = np.linspace(0, len(audio_data) / sample_rate, len(audio_data))
            plt.figure(figsize=(10, 4))
            plt.plot(time, audio_data)
            plt.title("Waveform")
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude")
            plt.show()
        except Exception as e:
            self.view.update_status(self.view.results_label, f"Error: {e}")

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

    def compute_rt60(self):
        try:
            low_band = (125, 500)
            mid_band = (500, 2000)
            high_band = (2000, 4000)

            rt60_low = self.model.compute_rt60_band(low_band)
            rt60_mid = self.model.compute_rt60_band(mid_band)
            rt60_high = self.model.compute_rt60_band(high_band)

            self.view.update_status(self.view.results_label, f"RT60 Low: {rt60_low:.2f}s, Mid: {rt60_mid:.2f}s, High: {rt60_high:.2f}s")
        except Exception as e:
            self.view.update_status(self.view.results_label, f"Error: {e}")

    def alternate_rt60_plots(self):
        try:
            frequency_bands = [
                ("Low (125-500 Hz)", (125, 500)),
                ("Mid (500-2000 Hz)", (500, 2000)),
                ("High (2000-4000 Hz)", (2000, 4000)),
            ]

            band_label, band_range = frequency_bands[self.view.current_band_index]
            self.view.current_band_index = (self.view.current_band_index + 1) % len(
                frequency_bands)  # Cycle through bands

            rt60_value = self.model.compute_rt60_band(band_range)
            filtered_audio = self.model.filter_audio_band(band_range)

            time = np.linspace(0, len(filtered_audio) / self.model.sample_rate, len(filtered_audio))
            plt.figure(figsize=(10, 4))
            plt.plot(time, filtered_audio, label=f"RT60: {rt60_value:.2f}s")
            plt.title(f"RT60 Plot - {band_label}")
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude")
            plt.legend()
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.view.update_status(self.view.results_label, f"Error: {e}")

    def combine_rt60_plots(self):
        try:
            frequency_bands = [
                ("Low (125-500 Hz)", (125, 500)),
                ("Mid (500-2000 Hz)", (500, 2000)),
                ("High (2000-4000 Hz)", (2000, 4000)),
            ]

            plt.figure(figsize=(10, 6))
            for band_label, band_range in frequency_bands:
                rt60_value = self.model.compute_rt60_band(band_range)
                filtered_audio = self.model.filter_audio_band(band_range)

                time = np.linspace(0, len(filtered_audio) / self.model.sample_rate, len(filtered_audio))
                plt.plot(time, filtered_audio, label=f"{band_label} RT60: {rt60_value:.2f}s")

            plt.title("Combined RT60 Plots")
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude")
            plt.legend()
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.view.update_status(self.view.results_label, f"Error: {e}")

    def show_highest_resonance(self):
        try:
            resonance = self.model.compute_resonant_frequency()
            self.view.update_status(self.view.results_label, f"Highest Resonance Frequency: {resonance:.2f} Hz")
        except Exception as e:
            self.view.update_status(self.view.results_label, f"Error: {e}")

    def show_rt60_difference(self):
        try:
            differences = self.model.compute_rt60_difference(target_rt60=0.5)
            result_text = "RT60 Differences (compared to 0.5 seconds):\n"
            for band, difference in differences.items():
                result_text += f"{band}: {difference:.2f} seconds\n"
            self.view.update_status(self.view.results_label, result_text)
        except Exception as e:
            self.view.update_status(self.view.results_label, f"Error: {e}")


if __name__ == "__main__":
    controller = AudioController()
    controller.view.run()

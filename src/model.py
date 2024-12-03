import os
import numpy as np
import librosa
from pydub import AudioSegment
class AudioModel:
    def __init__(self):
        self.audio_data = None
        self.sample_rate = None
        self.file_path = None

    def load_audio(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist.")

        # Convert non-WAV formats to WAV if needed
        if not file_path.endswith('.wav'):
            file_path = self._convert_to_wav(file_path)

        try:
            # Handle multi-channel audio by converting it to mono
            audio_data, sample_rate = librosa.load(file_path, sr=None, mono=False)
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=0)

            # Trim silence from the audio
            audio_trimmed, _ = librosa.effects.trim(audio_data)
            self.audio_data = audio_trimmed
            self.sample_rate = sample_rate
            self.file_path = file_path

            # Strip metadata
            audio = AudioSegment.from_file(file_path)
            audio.export(file_path, format="wav")

            return f"Audio loaded successfully: {file_path}, Sample Rate: {sample_rate}"
        except Exception as e:
            raise RuntimeError(f"Error loading audio file: {e}")

    def get_waveform(self):
        if self.audio_data is None:
            raise RuntimeError("No audio loaded. Please load an audio file first.")
        return self.audio_data, self.sample_rate

    @staticmethod
    def _convert_to_wav(file_path):
        try:
            audio = AudioSegment.from_file(file_path)
            wav_path = os.path.splitext(file_path)[0] + ".wav"
            audio.export(wav_path, format="wav")
            return wav_path
        except Exception as e:
            raise RuntimeError(f"Error converting to WAV: {e}")

    def compute_audio_duration(self):
        if self.audio_data is None:
            raise RuntimeError("No audio loaded. Please load an audio file first.")
        return len(self.audio_data) / self.sample_rate

    def compute_resonant_frequency(self):
        if self.audio_data is None:
            raise RuntimeError("No audio loaded. Please load an audio file first.")
        spectrum = np.fft.fft(self.audio_data)
        frequencies = np.fft.fftfreq(len(spectrum), d=1 / self.sample_rate)
        magnitude = np.abs(spectrum)
        peak_frequency = frequencies[np.argmax(magnitude)]
        return abs(peak_frequency)

    def compute_rt60_band(self, frequency_band):
        if self.audio_data is None:
            raise RuntimeError("No audio loaded. Please load an audio file first.")

        sos = butter(4, frequency_band, btype='bandpass', fs=self.sample_rate, output='sos')
        filtered_audio = sosfilt(sos, self.audio_data)

        energy = np.cumsum(filtered_audio[::-1] ** 2)[::-1]
        energy_db = 10 * np.log10(energy + 1e-10)

        peak_energy_db = np.max(energy_db)
        threshold_5db = peak_energy_db - 5
        threshold_25db = peak_energy_db - 25

        time_indices = np.linspace(0, len(filtered_audio) / self.sample_rate, len(filtered_audio))
        try:
            t_5db = time_indices[np.where(energy_db <= threshold_5db)[0][0]]
            t_25db = time_indices[np.where(energy_db <= threshold_25db)[0][0]]
        except IndexError:
            raise ValueError("Thresholds not reached in the audio.")

        rt60 = 2 * (t_25db - t_5db)
        return rt60

    def compute_rt60_difference(self, target_rt60=0.5):
        if self.audio_data is None:
            raise RuntimeError("No audio loaded. Please load an audio file first.")

        frequency_bands = {
            "Low (125-500 Hz)": (125, 500),
            "Mid (500-2000 Hz)": (500, 2000),
            "High (2000-4000 Hz)": (2000, 4000),
        }

        rt60_differences = {}
        for band_label, band_range in frequency_bands.items():
            rt60_value = self.compute_rt60_band(band_range)
            rt60_differences[band_label] = rt60_value - target_rt60

        return rt60_differences

    def filter_audio_band(self, frequency_band):
        """
        Filter audio for a given frequency band using a band-pass filter.
        """
        if self.audio_data is None:
            raise RuntimeError("No audio loaded. Please load an audio file first.")

        sos = butter(4, frequency_band, btype='bandpass', fs=self.sample_rate, output='sos')
        filtered_audio = sosfilt(sos, self.audio_data)
        return filtered_audio

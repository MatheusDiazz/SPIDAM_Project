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
    
    def compute_rt60(self):
        if self.audio_data is None:
            raise RuntimeError("No audio loaded. Please load an audio file first.")
        import numpy as np

        # Placeholder logic for RT60 calculation; implement proper logic if needed
        energy = np.cumsum(self.audio_data[::-1]**2)[::-1]
        # Compute energy decay curve
        energy = np.cumsum(self.audio_data[::-1] ** 2)[::-1]
        energy_db = 10 * np.log10(energy / np.max(energy))

        threshold_5db = np.where(energy_db <= -5)[0][0]
        threshold_35db = np.where(energy_db <= -35)[0][0]
        # Debug: Print energy decay curve
        print("Energy Decay (dB):", energy_db)
        # Check if energy decay curve has valid data
        if len(energy_db) == 0 or np.max(energy_db) == np.min(energy_db):
            raise ValueError("Energy decay curve is invalid. Audio may be silent or too short.")
        # Attempt to find absolute thresholds (-5 dB and -35 dB)
        thresholds_5db = np.where(energy_db <= -5)[0]
        thresholds_35db = np.where(energy_db <= -35)[0]
        if len(thresholds_5db) > 0 and len(thresholds_35db) > 0:
            # Use absolute thresholds if available
            threshold_5db = thresholds_5db[0]
            threshold_35db = thresholds_35db[0]
        else:
            # Fallback: Use dynamic thresholds based on the minimum decay level
            print("Using dynamic thresholds as absolute thresholds are not found.")
            min_db = np.min(energy_db)
            threshold_5db = np.where(energy_db <= min_db * 0.9)[0]
            threshold_35db = np.where(energy_db <= min_db * 0.7)[0]
            if len(threshold_5db) == 0 or len(threshold_35db) == 0:
                raise ValueError("Cannot determine RT60 due to insufficient decay.")
            threshold_5db = threshold_5db[0]
            threshold_35db = threshold_35db[0]
        # Calculate RT60
        time_5db = threshold_5db / self.sample_rate
        time_35db = threshold_35db / self.sample_rate
        rt60 = 2 * (time_35db - time_5db)
        print(f"RT60 Calculation Successful: {rt60:.2f} seconds")
        return rt60
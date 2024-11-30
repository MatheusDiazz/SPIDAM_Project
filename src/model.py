class AudioModel:
    def __init__(self):
        self.audio_data = None
        self.sample_rate = None
        self.file_path = None
    def load_audio(self, file_path):
        import os
        from pydub import AudioSegment
        import librosa

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist.")

        # Convert non-WAV formats to WAV if needed
        if not file_path.endswith('.wav'):
            file_path = self._convert_to_wav(file_path)

        # Load audio file using librosa
        try:
            self.audio_data, self.sample_rate = librosa.load(file_path, sr=None, mono=True)
            self.file_path = file_path
            return f"Audio loaded successfully: {file_path}, Sample Rate: {self.sample_rate}"
        except Exception as e:
            raise RuntimeError(f"Error loading audio file: {e}")
    @staticmethod
    def _convert_to_wav(file_path):
        from pydub import AudioSegment
        import os

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
        import numpy as np

        # Compute FFT to find peak frequency
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
        energy_db = 10 * np.log10(energy / np.max(energy))

        threshold_5db = np.where(energy_db <= -5)[0][0]
        threshold_35db = np.where(energy_db <= -35)[0][0]
        time_5db = threshold_5db / self.sample_rate
        time_35db = threshold_35db / self.sample_rate

        rt60 = 2 * (time_35db - time_5db)
        return rt60

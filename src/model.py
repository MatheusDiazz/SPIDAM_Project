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
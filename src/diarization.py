class DiarizationEngine:
    def __init__(self, model_name: str = "pyannote/speaker-diarization"):
        self.model_name = model_name

    def run(self, audio_path: str) -> list:
        # TODO: integrate pyannote pipeline
        return []
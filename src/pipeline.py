from dataclasses import dataclass
from pathlib import Path

@dataclass
class AudioJob:
    input_path: Path
    language: str = "en"

class VoicePipeline:
    def transcribe(self, job: AudioJob) -> dict:
        """Placeholder for Whisper + diarization"""
        raise NotImplementedError

    def summarize(self, transcript: dict) -> dict:
        """Placeholder for LLM summarization"""
        raise NotImplementedError
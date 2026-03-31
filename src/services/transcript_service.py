class TranscriptService:
    def __init__(self, store):
        self.store = store

    def save(self, job_id: str, transcript: dict):
        self.store[job_id] = transcript
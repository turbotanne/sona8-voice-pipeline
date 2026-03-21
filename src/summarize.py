class Summarizer:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

    def build_prompt(self, transcript: str) -> str:
        return f"Summarize this meeting:\n{transcript}"

    def run(self, transcript: str) -> dict:
        return {"summary": "TODO", "actions": []}
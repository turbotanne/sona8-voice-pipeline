from pathlib import Path

def load_audio(path: Path) -> bytes:
    with path.open(''rb'') as f:
        return f.read()

class IngestService:
    def submit(self, file_path: str) -> dict:
        data = load_audio(Path(file_path))
        # TODO: push to job queue
        return {"bytes": len(data)}
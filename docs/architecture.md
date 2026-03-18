# Architecture Overview

1. Ingest (Websocket, Batch Uploads)
2. Transcription (Whisper Medium, GPU pool)
3. Diarization (Pyannote 3.1, overlap handler)
4. Post-processing (summaries, sentiment, action extraction)
5. Delivery (JSON, Markdown, Slack webhooks)
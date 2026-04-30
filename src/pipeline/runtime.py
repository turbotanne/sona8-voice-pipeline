from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Dict, Iterable, List

StepFn = Callable[[Dict[str, Any]], Dict[str, Any]]


def _ingest(payload: Dict[str, Any]) -> Dict[str, Any]:
    payload.setdefault(metadata, {})
    payload[metadata][ingested_at] = datetime.utcnow().isoformat() + Z
    return payload


def _analyze(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = payload.get(text, ")

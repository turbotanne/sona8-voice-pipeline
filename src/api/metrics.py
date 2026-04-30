from __future__ import annotations

import json
import os
import pathlib
from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter

CACHE_ENV = SONA8_METRICS_CACHE
router = APIRouter()


def _load_cache() -> Dict[str, Any]:
    cache_path = os.environ.get(CACHE_ENV, metrics/latest.json)
    path = pathlib.Path(cache_path)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding=utf-8))
    except json.JSONDecodeError:
        return {}


def _with_defaults(cache: Dict[str, Any]) -> Dict[str, Any]:
    return {
        latency: cache.get(latency, {p50: 0.0, p95: 0.0}),
        queue_depth: cache.get(queue_depth, {current: 0, max: 0}),
        error_rate: cache.get(error_rate, {rolling_24h: 0.0}),
    }


@router.get(/metrics)
def get_metrics() -> Dict[str, Any]:
    cache = _load_cache()
    data = _with_defaults(cache)
    data[generated_at] = cache.get(generated_at, datetime.utcnow().isoformat() + Z)
    return data

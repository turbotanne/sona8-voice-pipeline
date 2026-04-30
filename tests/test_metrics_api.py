import json
import os
import pathlib

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.metrics import CACHE_ENV, router


def _build_app() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_metrics_endpoint_returns_keys(tmp_path, monkeypatch):
    cache = {
        "latency": {"p50": 1.2, "p95": 2.9},
        "queue_depth": {"current": 12, "max": 45},
        "error_rate": {"rolling_24h": 0.01},
        "generated_at": "2026-04-30T00:00:00Z",
    }
    cache_path = tmp_path / "latest.json"
    cache_path.write_text(json.dumps(cache), encoding="utf-8")
    monkeypatch.setenv(CACHE_ENV, str(cache_path))

    client = _build_app()
    response = client.get("/metrics")

    assert response.status_code == 200
    payload = response.json()
    assert payload["latency"]["p95"] == 2.9
    assert payload["queue_depth"]["current"] == 12
    assert payload["error_rate"]["rolling_24h"] == 0.01
    assert payload["generated_at"] == "2026-04-30T00:00:00Z"

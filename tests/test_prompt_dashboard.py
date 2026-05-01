from __future__ import annotations

import json
from pathlib import Path

from src.dashboard.prompt_dashboard import PromptDashboard, PromptSample


def test_dashboard_metrics(tmp_path: Path) -> None:
    samples = [
        {
            "prompt_id": "p1",
            "system_prompt": "act as assistant",
            "user_prompt": "hello",
            "response": "hi",
            "hallucination": False,
            "tokens": 12,
            "latency_ms": 120,
        },
        {
            "prompt_id": "p2",
            "system_prompt": "act as assistant",
            "user_prompt": "facts",
            "response": "wrong",
            "hallucination": True,
            "tokens": 25,
            "latency_ms": 400,
        },
    ]
    jsonl = tmp_path / "samples.jsonl"
    jsonl.write_text("\n".join(json.dumps(item) for item in samples), encoding="utf-8")

    dashboard = PromptDashboard.from_jsonl(str(jsonl))
    assert dashboard.hallucination_rate() == 0.5
    assert round(dashboard.average_tokens(), 1) == 18.5
    offenders = dashboard.worst_offenders(limit=1)
    assert offenders[0].prompt_id == "p2"


def test_prompt_sample_dataclass() -> None:
    sample = PromptSample.from_dict({
        "prompt_id": "demo",
        "system_prompt": "test",
        "user_prompt": "hello",
        "response": "world",
        "hallucination": False,
        "tokens": 10,
        "latency_ms": 50,
    })
    assert sample.prompt_id == "demo"
    assert sample.tokens == 10

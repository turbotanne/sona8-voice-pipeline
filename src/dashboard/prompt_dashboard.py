from __future__ import annotations

import json
import statistics
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


@dataclass
class PromptSample:
    """Represents a single prompt/response evaluation."""

    prompt_id: str
    system_prompt: str
    user_prompt: str
    response: str
    hallucination: bool
    tokens: int
    latency_ms: float

    @classmethod
    def from_dict(cls, payload: Dict[str, object]) -> "PromptSample":
        return cls(
            prompt_id=str(payload.get("prompt_id", "unknown")),
            system_prompt=str(payload.get("system_prompt", "")),
            user_prompt=str(payload.get("user_prompt", "")),
            response=str(payload.get("response", "")),
            hallucination=bool(payload.get("hallucination", False)),
            tokens=int(payload.get("tokens", 0)),
            latency_ms=float(payload.get("latency_ms", 0.0)),
        )


class PromptDashboard:
    """Aggregates prompt metrics for quality dashboards."""

    def __init__(self, samples: Optional[Iterable[PromptSample]] = None) -> None:
        self.samples: List[PromptSample] = list(samples or [])

    def add_sample(self, sample: PromptSample) -> None:
        self.samples.append(sample)

    @classmethod
    def from_jsonl(cls, path: str) -> "PromptDashboard":
        samples: List[PromptSample] = []
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                payload = json.loads(line)
                samples.append(PromptSample.from_dict(payload))
        return cls(samples)

    def hallucination_rate(self) -> float:
        if not self.samples:
            return 0.0
        flagged = sum(1 for sample in self.samples if sample.hallucination)
        return flagged / len(self.samples)

    def average_tokens(self) -> float:
        if not self.samples:
            return 0.0
        return statistics.fmean(sample.tokens for sample in self.samples)

    def average_latency(self) -> float:
        if not self.samples:
            return 0.0
        return statistics.fmean(sample.latency_ms for sample in self.samples)

    def worst_offenders(self, limit: int = 5) -> List[PromptSample]:
        return sorted(
            self.samples,
            key=lambda sample: (not sample.hallucination, -sample.latency_ms),
        )[:limit]

    def to_dict(self) -> Dict[str, object]:
        return {
            "total_samples": len(self.samples),
            "hallucination_rate": self.hallucination_rate(),
            "average_tokens": self.average_tokens(),
            "average_latency_ms": self.average_latency(),
        }

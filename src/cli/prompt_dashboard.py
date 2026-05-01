from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.dashboard.prompt_dashboard import PromptDashboard


def main() -> None:
    parser = argparse.ArgumentParser(description="Render prompt quality dashboard metrics")
    parser.add_argument("logs", help="Path to prompt JSONL file")
    parser.add_argument("--output", help="Optional JSON path to write the metrics")
    parser.add_argument("--top", type=int, default=5, help="Number of worst offenders to print")
    args = parser.parse_args()

    dashboard = PromptDashboard.from_jsonl(args.logs)
    metrics = dashboard.to_dict()

    print("Prompt Dashboard Metrics")
    print(json.dumps(metrics, indent=2))

    offenders = dashboard.worst_offenders(limit=args.top)
    if offenders:
        print("\nWorst offenders:")
        for sample in offenders:
            status = "HALLUCINATION" if sample.hallucination else "OK"
            print(f"- {sample.prompt_id}: {status}, latency={sample.latency_ms}ms, tokens={sample.tokens}")

    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"metrics": metrics}, indent=2), encoding="utf-8")
        print(f"Metrics written to {path}")


if __name__ == "__main__":
    main()

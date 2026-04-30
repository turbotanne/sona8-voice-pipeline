#!/usr/bin/env python3
"""Export queue + latency stats for reporting."""
from __future__ import annotations

import argparse
import json
import pathlib
from datetime import datetime
from urllib import request

DEFAULT_ENDPOINT = 'https://api.sona8.com/metrics'


def _fetch_metrics(endpoint: str) -> dict:
    with request.urlopen(endpoint, timeout=10) as response:
        payload = response.read().decode('utf-8')
    return json.loads(payload)


def _render_snapshot(data: dict) -> dict:
    now = datetime.utcnow().isoformat() + 'Z'
    return {
        'generated_at': now,
        'latency': data.get('latency', {}),
        'queue_depth': data.get('queue_depth', {}),
        'error_rate': data.get('error_rate', {}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Capture observability snapshot for weekly reports.')
    parser.add_argument('--endpoint', default=DEFAULT_ENDPOINT, help='Metrics endpoint to query')
    parser.add_argument('--output', default='reports/observability/latest.json', help='Destination path for the snapshot')
    parser.add_argument('--from-file', help='Optional path to reuse an existing metrics payload (skips HTTP call)')
    args = parser.parse_args()

    if args.from_file:
        raw = json.loads(pathlib.Path(args.from_file).read_text(encoding='utf-8'))
    else:
        raw = _fetch_metrics(args.endpoint)

    snapshot = _render_snapshot(raw)
    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(snapshot, indent=2), encoding='utf-8')
    print(f'Snapshot written to {output_path}')


if __name__ == '__main__':
    main()
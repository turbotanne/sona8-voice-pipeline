"""Batch summarization helper for Sona8."""
from __future__ import annotations

import argparse
import json
import pathlib
from datetime import datetime
from typing import Iterable

from src.pipeline.runtime import PipelineRuntime

SUPPORTED_SUFFIXES = {".txt", ".md", ".json"}


def _iter_inputs(folder: pathlib.Path, limit: int | None) -> Iterable[pathlib.Path]:
    count = 0
    for path in sorted(folder.rglob('*')):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        yield path
        count += 1
        if limit is not None and count >= limit:
            break


def _derive_output_path(base: pathlib.Path, target: pathlib.Path) -> pathlib.Path:
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    relative = target.with_suffix('').name
    return base / f"{timestamp}_{relative}.json"


def _summarize_text(text: str, runtime: PipelineRuntime) -> dict:
    payload = runtime.run_job(text)
    return {
        'summary': payload.get('summary', text[:280]),
        'metadata': payload.get('metadata', {}),
        'word_count': len(text.split()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Batch summarization utility for Sona8 demos.')
    parser.add_argument('--input', required=True, help='Folder that contains .txt/.md/.json inputs')
    parser.add_argument('--output', default='reports/batch', help='Destination folder for JSON summaries')
    parser.add_argument('--limit', type=int, help='Optional maximum number of files to process')
    parser.add_argument('--dry-run', action='store_true', help='Print summaries instead of writing files')
    args = parser.parse_args()

    input_dir = pathlib.Path(args.input).expanduser()
    if not input_dir.exists():
        raise SystemExit(f'Input folder {input_dir} does not exist')

    output_dir = pathlib.Path(args.output).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    runtime = PipelineRuntime()
    processed = 0
    for file_path in _iter_inputs(input_dir, args.limit):
        text = file_path.read_text(encoding='utf-8')
        summary = _summarize_text(text, runtime)
        processed += 1
        if args.dry_run:
            print(json.dumps({'file': str(file_path), **summary}, indent=2))
            continue
        destination = _derive_output_path(output_dir, file_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(summary, indent=2), encoding='utf-8')
        print(f'Wrote {destination}')

    print(f'Processed {processed} files from {input_dir}')


if __name__ == '__main__':
    main()
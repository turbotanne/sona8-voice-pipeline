"""Validate pipeline configuration files before deployment."""
from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

REQUIRED_KEYS = {'max_latency', 'autoscale', 'feature_flags'}


def _load_document(path: pathlib.Path) -> Dict[str, Any]:
    text = path.read_text(encoding='utf-8')
    if path.suffix in {'.yaml', '.yml'}:
        if yaml is None:
            raise RuntimeError('pyyaml is required to lint YAML files')
        return yaml.safe_load(text) or {}
    if path.suffix == '.json':
        return json.loads(text)
    raise RuntimeError(f'Unsupported config type: {path.suffix}')


def _collect_issues(doc: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    missing = REQUIRED_KEYS - doc.keys()
    if missing:
        issues.append(f'Missing required keys: {", ".join(sorted(missing))}')
    latency = doc.get('max_latency')
    if isinstance(latency, (int, float)) and latency > 6.0:
        issues.append('max_latency exceeds 6 seconds SLA')
    flags = doc.get('feature_flags', {})
    if isinstance(flags, dict):
        stale = [name for name, value in flags.items() if value == 'deprecated']
        if stale:
            issues.append(f'Found deprecated feature flags: {", ".join(stale)}')
    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description='Lint pipeline configuration files for common pitfalls.')
    parser.add_argument('--file', required=True, help='Path to pipeline.yaml / pipeline.json')
    args = parser.parse_args()

    config_path = pathlib.Path(args.file)
    if not config_path.exists():
        raise SystemExit(f'Config file {config_path} not found')

    document = _load_document(config_path)
    issues = _collect_issues(document)
    if issues:
        print('âœ– Config failed validation:')
        for issue in issues:
            print(f'  - {issue}')
        raise SystemExit(1)

    print(f'âœ” {config_path} passed validation')


if __name__ == '__main__':
    main()
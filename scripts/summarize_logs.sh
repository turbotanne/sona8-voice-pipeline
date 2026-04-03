#!/usr/bin/env bash
set -euo pipefail
grep -R "ERROR" logs > logs/errors.txt
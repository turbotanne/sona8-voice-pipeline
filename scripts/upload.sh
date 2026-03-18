#!/usr/bin/env bash
set -euo pipefail
FILE="$1"
TOKEN="$SONA8_API_TOKEN"
curl -X POST "https://api.sona8.com/jobs" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@${FILE}"
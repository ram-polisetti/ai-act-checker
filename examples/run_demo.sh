#!/usr/bin/env bash
# End-to-end demo: classify 5 example systems spanning every EU AI Act tier.
set -u
cd "$(dirname "$0")/.."
export PYTHONPATH=src
PY=/tmp/actvenv/bin/python
LOG=demo-assessments.jsonl
rm -f "$LOG"

run() {
  echo "=== $1 ==="
  $PY -m aiact.cli assess --input "examples/$1.json" --log "$LOG" --out "examples/$1.report.json"
  echo "exit code: $?"
  echo
}

run social-scoring
run hire-screen
run support-chatbot
run spam-filter
run gpai-frontier

echo "=== audit log verification ==="
$PY -m aiact.cli verify-log --log "$LOG"

"""Append-only hash-chained JSONL audit log for assessments.

Each record carries: timestamp (UTC), the SHA-256 of the canonical input,
the assessment, the previous record's hash, and its own hash. Tampering
with any record breaks the chain, which `verify_log` detects. Same
pattern as Charan's opsaudit / rai-monitor tooling.
"""

import hashlib
import json
import os
from datetime import datetime, timezone

LOG_VERSION = 1


def _utcnow():
    return datetime.now(timezone.utc).isoformat()


def _canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def _hash_record(record_without_hash):
    return hashlib.sha256(_canonical(record_without_hash).encode("utf-8")).hexdigest()


def _last_hash(path):
    if not os.path.exists(path):
        return "GENESIS"
    last = None
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                last = line
    if last is None:
        return "GENESIS"
    return json.loads(last)["hash"]


def append_assessment(path, system_desc, assessment):
    """Append an assessment to the log. Returns the stored record."""
    prev = _last_hash(path)
    record = {
        "log_version": LOG_VERSION,
        "timestamp": _utcnow(),
        "input_sha256": hashlib.sha256(
            _canonical(system_desc).encode("utf-8")
        ).hexdigest(),
        "system_name": assessment.get("system_name"),
        "risk_tier": assessment.get("risk_tier"),
        "assessment": assessment,
        "prev_hash": prev,
    }
    record["hash"] = _hash_record(record)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(_canonical(record) + "\n")
    return record


def verify_log(path):
    """Verify the hash chain. Returns (ok, checked, error)."""
    if not os.path.exists(path):
        return True, 0, None
    prev = "GENESIS"
    checked = 0
    with open(path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                return False, checked, f"line {lineno}: invalid JSON ({exc})"
            if record.get("prev_hash") != prev:
                return (
                    False,
                    checked,
                    f"line {lineno}: prev_hash mismatch (chain broken)",
                )
            stored = record.pop("hash", None)
            recomputed = _hash_record(record)
            record["hash"] = stored
            if stored != recomputed:
                return (
                    False,
                    checked,
                    f"line {lineno}: record hash mismatch (tampered)",
                )
            prev = stored
            checked += 1
    return True, checked, None

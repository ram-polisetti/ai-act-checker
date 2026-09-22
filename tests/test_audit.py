"""Tests for the hash-chained audit log."""

import json
import os

import pytest

from aiact.audit import append_assessment, verify_log
from aiact.classify import classify


def assess(name="S", **kw):
    d = {"name": name}
    d.update(kw)
    return d, classify(d)


def test_append_and_verify(tmp_path):
    log = str(tmp_path / "audit.jsonl")
    d, a = assess("One")
    rec = append_assessment(log, d, a)
    assert rec["prev_hash"] == "GENESIS"
    assert len(rec["hash"]) == 64
    ok, checked, err = verify_log(log)
    assert ok and checked == 1 and err is None


def test_chain_links_records(tmp_path):
    log = str(tmp_path / "audit.jsonl")
    recs = []
    for name in ("One", "Two", "Three"):
        d, a = assess(name)
        recs.append(append_assessment(log, d, a))
    assert recs[1]["prev_hash"] == recs[0]["hash"]
    assert recs[2]["prev_hash"] == recs[1]["hash"]
    ok, checked, _ = verify_log(log)
    assert ok and checked == 3


def test_tamper_detected(tmp_path):
    log = str(tmp_path / "audit.jsonl")
    d, a = assess("One", social_scoring=True)
    append_assessment(log, d, a)
    d2, a2 = assess("Two")
    append_assessment(log, d2, a2)
    # tamper with the first record's tier
    lines = open(log).read().splitlines()
    rec = json.loads(lines[0])
    assert rec["assessment"]["risk_tier"] == "prohibited"
    rec["assessment"]["risk_tier"] = "minimal-risk"
    rec["risk_tier"] = "minimal-risk"
    lines[0] = json.dumps(rec, sort_keys=True)
    open(log, "w").write("\n".join(lines) + "\n")
    ok, checked, err = verify_log(log)
    assert not ok
    assert "tampered" in err or "mismatch" in err


def test_broken_link_detected(tmp_path):
    log = str(tmp_path / "audit.jsonl")
    d, a = assess("One")
    append_assessment(log, d, a)
    d2, a2 = assess("Two")
    append_assessment(log, d2, a2)
    lines = open(log).read().splitlines()
    # delete the first record entirely -> second record's prev_hash dangles
    open(log, "w").write(lines[1] + "\n")
    ok, checked, err = verify_log(log)
    assert not ok
    assert "prev_hash" in err


def test_verify_missing_log_ok(tmp_path):
    ok, checked, err = verify_log(str(tmp_path / "nope.jsonl"))
    assert ok and checked == 0


def test_record_carries_input_hash_and_tier(tmp_path):
    log = str(tmp_path / "audit.jsonl")
    d, a = assess("Scorer", social_scoring=True)
    rec = append_assessment(log, d, a)
    assert rec["risk_tier"] == "prohibited"
    assert len(rec["input_sha256"]) == 64
    assert rec["timestamp"]

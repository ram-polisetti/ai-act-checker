"""Tests for the CLI: exit codes, JSON output, log verification."""

import json
import subprocess
import sys

import pytest

from aiact.cli import main


def run_cli(tmp_path, desc, extra=()):
    inp = tmp_path / "in.json"
    inp.write_text(json.dumps(desc))
    log = tmp_path / "audit.jsonl"
    out = tmp_path / "report.json"
    code = main(
        ["assess", "--input", str(inp), "--log", str(log), "--out", str(out),
         "--quiet", *extra]
    )
    return code, json.loads(out.read_text()), log


def test_cli_prohibited_exit_2(tmp_path):
    code, report, log = run_cli(tmp_path, {"name": "S", "social_scoring": True})
    assert code == 2
    assert report["risk_tier"] == "prohibited"
    assert log.exists()


def test_cli_high_risk_exit_1(tmp_path):
    code, report, _ = run_cli(
        tmp_path, {"name": "H", "use_case_tags": ["cv_screening"]})
    assert code == 1
    assert report["risk_tier"] == "high-risk"


def test_cli_limited_exit_0(tmp_path):
    code, report, _ = run_cli(
        tmp_path, {"name": "C", "interacts_with_persons": True})
    assert code == 0
    assert report["risk_tier"] == "limited-risk"


def test_cli_minimal_exit_0(tmp_path):
    code, report, _ = run_cli(tmp_path, {"name": "M"})
    assert code == 0
    assert report["risk_tier"] == "minimal-risk"


def test_cli_verify_log_ok(tmp_path):
    _, _, log = run_cli(tmp_path, {"name": "M"})
    assert main(["verify-log", "--log", str(log)]) == 0


def test_cli_verify_log_missing_ok(tmp_path):
    assert main(["verify-log", "--log", str(tmp_path / "nope.jsonl")]) == 0


def test_cli_bad_input_exits_3(tmp_path):
    assert main(["assess", "--input", str(tmp_path / "missing.json")]) == 3


def test_cli_report_is_complete_json(tmp_path):
    _, report, _ = run_cli(
        tmp_path,
        {"name": "H", "gpai_model": True, "training_compute_flop": 3e25,
         "use_case_tags": ["cv_screening"]},
    )
    for key in ("system_name", "risk_tier", "exit_code", "findings",
                "transparency_obligations", "gpai_analysis",
                "conformity_checklist", "act", "disclaimer"):
        assert key in report
    assert report["gpai_analysis"]["systemic_risk"] is True

"""CLI for the EU AI Act conformity checker.

Commands:
  act-checker assess --input system.yaml [--log audit.jsonl] [--out report.json]
  act-checker verify-log --log audit.jsonl
  act-checker tags            # list recognised use-case tags

Exit codes for `assess`: 0 = minimal/limited risk, 1 = high-risk
(obligations apply), 2 = prohibited practice. Any CLI usage error exits 3.
"""

import argparse
import json
import sys

from .classify import classify, EXIT_CODES
from .audit import append_assessment, verify_log
from . import knowledge as K

DEFAULT_LOG = "assessments.jsonl"


def _load_input(path):
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    try:
        import yaml  # type: ignore
    except ImportError:
        raise SystemExit(
            "Input is not JSON and PyYAML is not installed; "
            "provide JSON or install pyyaml."
        )
    return yaml.safe_load(text)


def _print_human(assessment):
    tier = assessment["risk_tier"].upper()
    print(f"System: {assessment['system_name']}")
    print(f"Risk tier: {tier}")
    for f in assessment["findings"]:
        print(f"  - [{f['article']}] {f['title']}")
    for o in assessment["transparency_obligations"]:
        print(f"  - [{o['article']}] {o['title']}")
    gpai = assessment.get("gpai_analysis")
    if gpai:
        sr = "SYSTEMIC RISK" if gpai["systemic_risk"] else "no systemic risk"
        print(f"  GPAI model: yes ({sr})")
        if gpai["systemic_risk_basis"]:
            print(f"    {gpai['systemic_risk_basis']}")
    n_check = len(assessment["conformity_checklist"])
    if n_check:
        print(f"  Conformity checklist: {n_check} items (see JSON report)")


def cmd_assess(args):
    desc = _load_input(args.input)
    if not isinstance(desc, dict):
        raise SystemExit("Input must be a mapping describing one AI system.")
    assessment = classify(desc)
    record = append_assessment(args.log, desc, assessment)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(assessment, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    if not args.quiet:
        _print_human(assessment)
        print(f"Logged to {args.log} (record {record['hash'][:12]})")
    return assessment["exit_code"]


def cmd_verify_log(args):
    ok, checked, error = verify_log(args.log)
    if ok:
        print(f"OK: {checked} record(s), chain intact ({args.log})")
        return 0
    print(f"FAIL: {error}")
    return 1


def cmd_tags(_args):
    tags = sorted(
        {kw for area in K.ANNEX_III_AREAS for kw in area["keywords"]}
    )
    print("Recognised Annex III use-case tags:")
    for t in tags:
        print(f"  {t}")
    print("\nBoolean flags: " + ", ".join(sorted(__import__("aiact.classify", fromlist=["SCHEMA_FLAGS"]).SCHEMA_FLAGS)))
    return 0


def build_parser():
    p = argparse.ArgumentParser(
        prog="act-checker",
        description="EU AI Act conformity checker — risk-tier triage with citations.",
    )
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("assess", help="Classify a system description.")
    a.add_argument("--input", required=True, help="YAML or JSON system description.")
    a.add_argument("--log", default=DEFAULT_LOG, help="Audit log path (JSONL).")
    a.add_argument("--out", default=None, help="Write the JSON report here.")
    a.add_argument("--quiet", action="store_true", help="Suppress human summary.")
    a.set_defaults(func=cmd_assess)

    v = sub.add_parser("verify-log", help="Verify an audit log's hash chain.")
    v.add_argument("--log", default=DEFAULT_LOG)
    v.set_defaults(func=cmd_verify_log)

    t = sub.add_parser("tags", help="List recognised use-case tags and flags.")
    t.set_defaults(func=cmd_tags)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 3
    except SystemExit as exc:
        # _load_input raises SystemExit with a message on bad input
        if exc.code:
            print(f"Error: {exc.code}", file=sys.stderr)
            return 3
        return 0


if __name__ == "__main__":
    sys.exit(main())

# ai-act-checker

A deterministic **EU AI Act conformity checker**: describe an AI system, get back a risk-tier workup with citations to the actual Act — prohibited practices (Article 5), high-risk use cases (Article 6 + Annex III), transparency duties (Article 50), and GPAI / systemic-risk duties (Articles 51–55). Every assessment lands in a hash-chained, append-only audit log.

Built by an operator, for operators. Part of the [opsaudit](https://github.com/ram-polisetti/opsaudit) governance tooling family.

## Quickstart

```bash
pip install -e .
act-checker assess --input examples/hire-screen.json --out report.json
echo "exit: $?"   # 0 = minimal/limited · 1 = high-risk · 2 = prohibited
act-checker verify-log --log assessments.jsonl
```

Describe a system in JSON (or YAML) — see `examples/`:

```json
{
  "name": "HireScreen CV Ranker",
  "provider_role": "provider",
  "intended_purpose": "Rank job applicants by CV for first-round screening",
  "use_case_tags": ["cv_screening", "candidate_evaluation"],
  "interacts_with_persons": true
}
```

`act-checker tags` lists every recognised Annex III use-case tag and boolean flag.

## What you get

- **Risk tier** — prohibited / high-risk / limited-risk / minimal-risk, with the specific Article 5(1)(a)–(h) prohibition, Annex III point, or Article 50 duty cited for each determination.
- **GPAI analysis** — provider duties (Article 53) and, when cumulative training compute exceeds the Article 51(2) presumption threshold of 10²⁵ FLOP, systemic-risk duties (Article 55).
- **Conformity checklist** — for high-risk systems, the Chapter III Section 2 requirements (Articles 9–15) plus provider, deployer, FRIA, conformity-assessment, registration and post-market duties, each citing its article.
- **Audit log** — every assessment appended to a SHA-256 hash-chained JSONL log; `verify-log` detects tampering or broken links.

## Methodology & limitations

See [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for the legal source text, how the rules were derived, and what the tool does **not** do (it is a triage aid, not legal advice).

## Tests

```bash
pip install pytest
PYTHONPATH=src python -m pytest tests/ -q   # 48/48
```

## License

Apache-2.0 — see [LICENSE](LICENSE).

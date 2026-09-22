# Methodology, data sources, and limitations

## Legal source

All rules in `src/aiact/knowledge.py` were derived from the official
English text of **Regulation (EU) 2024/1689** (the EU Artificial
Intelligence Act), retrieved from EUR-Lex on 2026-09-22:

- Source URL: <https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202401689>
- Citation: OJ L 2024/1689
- A verbatim copy of the retrieved text is kept at `eu_ai_act.txt`
  (working copy; not shipped as part of the package).

Every rule carries its article citation (e.g. `Article 5(1)(c)`,
`Annex III, point 4(a)-(b)`, `Article 51(2)`). Determinations can be
checked against the source text paragraph by paragraph.

## How the classifier works

1. **Prohibited (Article 5)** is evaluated first: eight rules mirroring
   Article 5(1)(a)–(h). Each fires only when its full conjunction of
   input flags holds (e.g. 5(1)(f) needs `emotion_inference` *and* a
   workplace/education context; 5(1)(h) needs real-time remote biometric
   ID *and* public space *and* law-enforcement use).
2. **High-risk (Article 6)** next: Annex III use-case tags matched
   against the eight areas of Annex III (points 1–8), plus the
   Article 6(1) safety-component flag for Annex I product legislation.
3. **Limited-risk (Article 50)** next: four transparency duties —
   50(1) AI-interaction disclosure, 50(2) machine-readable marking of
   synthetic content, 50(3) notice for emotion recognition / biometric
   categorisation, 50(4) deepfake disclosure.
4. **GPAI (Articles 51–55)** is analysed independently of the risk tier:
   provider duties (Article 53, Annexes XI–XII), open-source note
   (Article 53(2)), and systemic-risk duties (Article 55) when the
   Article 51(2) presumption — cumulative training compute greater than
   10²⁵ FLOP — is met.
5. Anything matching none of the above is **minimal risk**.

The engine is fully deterministic and needs no model; classification is
covered by `tests/test_classify.py` and `tests/test_gpai.py`.

## What this tool does not do

- **Not legal advice.** The checker is a triage aid. It cannot assess
  Article 6(3) derogations (an Annex III system that does not pose
  significant risk), Article 5 exceptions and authorisation regimes,
  sectoral carve-outs, or transitional provisions (Article 113). Any
  real conformity decision needs qualified counsel.
- **Tags are a simplification.** Real systems need a factual analysis of
  intended purpose; the tag list is a navigation aid, not an
  interpretation of the Annex.
- **Static knowledge.** The Commission can amend Annex III by delegated
  act (Article 7) and the GPAI thresholds (Article 51(3)); the
  `knowledge_date` field records which snapshot the rules encode.
- **No LLM involved.** Narrative summaries are not generated; outputs
  are rule citations plus short paraphrases.

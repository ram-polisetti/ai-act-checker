"""Deterministic EU AI Act risk-tier classification engine.

Input: a system description dict (see SCHEMA below). The engine evaluates
rules in tier order — prohibited (Article 5) first, then high-risk
(Article 6 + Annex III / Annex I), then limited-risk transparency duties
(Article 50), then GPAI analysis (Articles 51-55), defaulting to
minimal risk. Classification itself never needs a model; it is fully
testable.
"""

from . import knowledge as K

TIER_PROHIBITED = "prohibited"
TIER_HIGH = "high-risk"
TIER_LIMITED = "limited-risk"
TIER_MINIMAL = "minimal-risk"

TIER_ORDER = [TIER_PROHIBITED, TIER_HIGH, TIER_LIMITED, TIER_MINIMAL]

EXIT_CODES = {
    TIER_PROHIBITED: 2,
    TIER_HIGH: 1,
    TIER_LIMITED: 0,
    TIER_MINIMAL: 0,
}

# Boolean flags understood by the rule engine. Anything not listed here is
# ignored (forward-compatible with richer descriptions).
SCHEMA_FLAGS = [
    # --- Article 5 prohibition flags ---
    "manipulative_techniques",
    "exploits_vulnerability",
    "social_scoring",
    "crime_risk_assessment",
    "untargeted_facial_scraping",
    "emotion_inference",
    "biometric_categorisation_sensitive",
    "real_time_remote_biometric_id",
    # --- context flags used by prohibition rules ---
    "workplace",
    "education",
    "public_space",
    "law_enforcement",
    # --- Article 6(1): safety component under Annex I product legislation ---
    "annex_i_safety_component",
    # --- Article 50 transparency flags ---
    "interacts_with_persons",
    "generates_synthetic_content",
    "emotion_recognition_deployed",
    "biometric_categorisation_deployed",
    "deepfake",
    # --- GPAI flags ---
    "gpai_model",
    "training_compute_flop",
    "open_source",
]


def _flag(desc, name):
    return bool(desc.get(name, False))


def _rule_matches(rule, desc):
    for name in rule.get("all_of", []):
        if not _flag(desc, name):
            return False
    any_of = rule.get("any_of", [])
    if any_of and not any(_flag(desc, n) for n in any_of):
        return False
    return True


def check_prohibitions(desc):
    """Return the list of matched Article 5 prohibition rules."""
    return [r for r in K.PROHIBITIONS if _rule_matches(r, desc)]


def check_annex_iii(desc):
    """Return matched Annex III high-risk areas for the use-case tags."""
    tags = set(desc.get("use_case_tags", []) or [])
    matched = []
    for area in K.ANNEX_III_AREAS:
        hits = [kw for kw in area["keywords"] if kw in tags]
        if hits:
            matched.append({**area, "matched_tags": hits})
    return matched


def check_annex_i(desc):
    return _flag(desc, "annex_i_safety_component")


def check_transparency(desc):
    """Return matched Article 50 transparency obligations."""
    return [r for r in K.TRANSPARENCY_RULES if _rule_matches(r, desc)]


def analyse_gpai(desc):
    """GPAI analysis per Articles 51-55. Returns None if not a GPAI model."""
    if not _flag(desc, "gpai_model"):
        return None
    flop = desc.get("training_compute_flop")
    systemic = False
    systemic_basis = None
    if flop is not None:
        try:
            flop = float(flop)
        except (TypeError, ValueError):
            flop = None
    if flop is not None and flop > K.SYSTEMIC_RISK_FLOP_THRESHOLD:
        systemic = True
        systemic_basis = (
            f"Cumulative training compute {flop:.3g} FLOP exceeds the "
            f"Article 51(2) presumption threshold of 1e25 FLOP."
        )
    return {
        "is_gpai_model": True,
        "training_compute_flop": flop,
        "systemic_risk": systemic,
        "systemic_risk_basis": systemic_basis,
        "provider_duties": [
            {"article": d["article"], "duty": d["duty"]}
            for d in K.GPAI_PROVIDER_DUTIES
        ],
        "systemic_risk_duties": (
            [
                {"article": d["article"], "duty": d["duty"]}
                for d in K.SYSTEMIC_RISK_DUTIES
            ]
            if systemic
            else []
        ),
        "open_source": _flag(desc, "open_source"),
    }


def high_risk_checklist():
    """The Section 2 conformity checklist for high-risk systems."""
    return [
        {"article": c["article"], "item": c["item"], "detail": c["detail"]}
        for c in K.HIGH_RISK_CHECKLIST
    ]


def classify(desc):
    """Classify a system description. Returns a full assessment dict."""
    name = desc.get("name", "unnamed system")

    prohibitions = check_prohibitions(desc)
    annex_iii = check_annex_iii(desc)
    annex_i = check_annex_i(desc)
    transparency = check_transparency(desc)
    gpai = analyse_gpai(desc)

    if prohibitions:
        tier = TIER_PROHIBITED
    elif annex_iii or annex_i:
        tier = TIER_HIGH
    elif transparency:
        tier = TIER_LIMITED
    else:
        tier = TIER_MINIMAL

    findings = []
    for r in prohibitions:
        findings.append(
            {
                "tier": TIER_PROHIBITED,
                "rule_id": r["id"],
                "article": r["article"],
                "title": r["title"],
                "description": r["description"],
            }
        )
    if annex_i:
        a = K.ANNEX_I_SAFETY_COMPONENT
        findings.append(
            {
                "tier": TIER_HIGH,
                "rule_id": "H-annex-i",
                "article": a["article"],
                "title": a["title"],
                "description": a["description"],
            }
        )
    for area in annex_iii:
        findings.append(
            {
                "tier": TIER_HIGH,
                "rule_id": "H-" + area["point"].replace(", ", "-").replace(" ", "-").lower(),
                "article": "Article 6(2); " + area["citation"],
                "title": "High-risk use case: " + area["area"],
                "description": area["description"],
                "matched_tags": area["matched_tags"],
            }
        )
    obligations = []
    for r in transparency:
        obligations.append(
            {
                "rule_id": r["id"],
                "article": r["article"],
                "title": r["title"],
                "description": r["description"],
            }
        )

    assessment = {
        "system_name": name,
        "risk_tier": tier,
        "exit_code": EXIT_CODES[tier],
        "findings": findings,
        "transparency_obligations": obligations,
        "gpai_analysis": gpai,
        "conformity_checklist": high_risk_checklist() if tier == TIER_HIGH else [],
        "act": K.ACT_CITATION,
        "act_source": K.ACT_SOURCE_URL,
        "knowledge_date": K.KNOWLEDGE_DATE,
        "disclaimer": (
            "Automated triage aid, not legal advice. Verify every "
            "determination against the official Act text and consult "
            "qualified counsel before placing a system on the market."
        ),
    }
    return assessment

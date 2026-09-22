"""Tests for the deterministic classification engine."""

import pytest

from aiact.classify import classify, EXIT_CODES


def desc(**kw):
    base = {"name": "test system"}
    base.update(kw)
    return base


# --- Prohibited practices (Article 5) ---------------------------------------

def test_social_scoring_is_prohibited():
    a = classify(desc(social_scoring=True))
    assert a["risk_tier"] == "prohibited"
    arts = [f["article"] for f in a["findings"]]
    assert "Article 5(1)(c)" in arts
    assert a["exit_code"] == 2


def test_manipulative_techniques_prohibited():
    a = classify(desc(manipulative_techniques=True))
    assert a["risk_tier"] == "prohibited"
    assert any(f["rule_id"] == "P-a" for f in a["findings"])


def test_vulnerability_exploitation_prohibited():
    a = classify(desc(exploits_vulnerability=True))
    assert a["risk_tier"] == "prohibited"
    assert any(f["article"] == "Article 5(1)(b)" for f in a["findings"])


def test_predictive_policing_prohibited():
    a = classify(desc(crime_risk_assessment=True))
    assert a["risk_tier"] == "prohibited"
    assert any(f["article"] == "Article 5(1)(d)" for f in a["findings"])


def test_untargeted_facial_scraping_prohibited():
    a = classify(desc(untargeted_facial_scraping=True))
    assert a["risk_tier"] == "prohibited"
    assert any(f["article"] == "Article 5(1)(e)" for f in a["findings"])


def test_workplace_emotion_inference_prohibited():
    a = classify(desc(emotion_inference=True, workplace=True))
    assert a["risk_tier"] == "prohibited"
    assert any(f["article"] == "Article 5(1)(f)" for f in a["findings"])


def test_emotion_inference_without_context_not_prohibited():
    # Art 5(1)(f) needs the workplace/education context; without it the
    # system falls through to transparency duties instead.
    a = classify(
        desc(emotion_inference=True, emotion_recognition_deployed=True)
    )
    assert a["risk_tier"] != "prohibited"


def test_sensitive_biometric_categorisation_prohibited():
    a = classify(desc(biometric_categorisation_sensitive=True))
    assert a["risk_tier"] == "prohibited"
    assert any(f["article"] == "Article 5(1)(g)" for f in a["findings"])


def test_realtime_rbi_public_law_enforcement_prohibited():
    a = classify(
        desc(
            real_time_remote_biometric_id=True,
            public_space=True,
            law_enforcement=True,
        )
    )
    assert a["risk_tier"] == "prohibited"
    assert any(f["article"] == "Article 5(1)(h)" for f in a["findings"])


def test_realtime_rbi_without_le_context_not_prohibited():
    # Without the law-enforcement + public-space conjunction it is not
    # the Article 5(1)(h) prohibition (it may still be high-risk RBI).
    a = classify(desc(real_time_remote_biometric_id=True))
    assert a["risk_tier"] != "prohibited"


def test_prohibition_beats_high_risk():
    # A system matching both a prohibition and an Annex III use case must
    # land in the prohibited tier.
    a = classify(
        desc(social_scoring=True, use_case_tags=["recruitment", "cv_screening"])
    )
    assert a["risk_tier"] == "prohibited"


# --- High-risk (Article 6 + Annex III) --------------------------------------

def test_cv_screening_high_risk_employment():
    a = classify(
        desc(
            name="HireScreen",
            use_case_tags=["cv_screening", "candidate_evaluation"],
        )
    )
    assert a["risk_tier"] == "high-risk"
    assert a["exit_code"] == 1
    arts = [f["article"] for f in a["findings"]]
    assert any("Annex III, point 4" in art for art in arts)
    assert len(a["conformity_checklist"]) > 0


def test_credit_scoring_high_risk():
    a = classify(desc(use_case_tags=["creditworthiness"]))
    assert a["risk_tier"] == "high-risk"
    assert any("Annex III, point 5" in f["article"] for f in a["findings"])


def test_exam_proctoring_high_risk_education():
    a = classify(desc(use_case_tags=["exam_proctoring"]))
    assert a["risk_tier"] == "high-risk"
    assert any("Annex III, point 3" in f["article"] for f in a["findings"])


def test_annex_i_safety_component_high_risk():
    a = classify(desc(annex_i_safety_component=True))
    assert a["risk_tier"] == "high-risk"
    assert any(f["article"] == "Article 6(1)" for f in a["findings"])


def test_multiple_annex_iii_areas_all_cited():
    a = classify(
        desc(use_case_tags=["cv_screening", "creditworthiness"])
    )
    assert a["risk_tier"] == "high-risk"
    arts = " ".join(f["article"] for f in a["findings"])
    assert "point 4" in arts and "point 5" in arts


# --- Limited risk (Article 50 transparency) ---------------------------------

def test_chatbot_limited_risk():
    a = classify(desc(name="SupportBot", interacts_with_persons=True))
    assert a["risk_tier"] == "limited-risk"
    assert a["exit_code"] == 0
    arts = [o["article"] for o in a["transparency_obligations"]]
    assert "Article 50(1)" in arts


def test_synthetic_content_generator_limited_risk():
    a = classify(desc(generates_synthetic_content=True))
    assert a["risk_tier"] == "limited-risk"
    assert any(
        o["article"] == "Article 50(2)"
        for o in a["transparency_obligations"]
    )


def test_deepfake_deployer_disclosure():
    a = classify(desc(deepfake=True))
    assert a["risk_tier"] == "limited-risk"
    assert any(
        o["article"] == "Article 50(4)"
        for o in a["transparency_obligations"]
    )


def test_high_risk_beats_transparency_tier():
    # A high-risk system that also chats with users is still high-risk;
    # transparency duties are reported alongside.
    a = classify(
        desc(use_case_tags=["cv_screening"], interacts_with_persons=True)
    )
    assert a["risk_tier"] == "high-risk"
    assert any(
        o["article"] == "Article 50(1)"
        for o in a["transparency_obligations"]
    )


# --- Minimal risk ------------------------------------------------------------

def test_spam_filter_minimal_risk():
    a = classify(desc(name="SpamFilter"))
    assert a["risk_tier"] == "minimal-risk"
    assert a["exit_code"] == 0
    assert a["findings"] == []
    assert a["transparency_obligations"] == []
    assert a["conformity_checklist"] == []


def test_unknown_flags_ignored():
    a = classify(desc(name="X", some_future_flag=True))
    assert a["risk_tier"] == "minimal-risk"


def test_every_assessment_carries_act_citation():
    a = classify(desc())
    assert "2024/1689" in a["act"]
    assert a["act_source"].startswith("https://eur-lex.europa.eu")
    assert "not legal advice" in a["disclaimer"]

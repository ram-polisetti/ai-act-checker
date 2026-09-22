"""Tests for GPAI analysis (Articles 51-55) and the conformity checklist."""

from aiact.classify import classify, high_risk_checklist
from aiact import knowledge as K


def test_non_gpai_has_no_gpai_analysis():
    a = classify({"name": "plain classifier"})
    assert a["gpai_analysis"] is None


def test_gpai_model_gets_provider_duties():
    a = classify({"name": "BaseModel", "gpai_model": True})
    g = a["gpai_analysis"]
    assert g is not None
    assert g["is_gpai_model"] is True
    assert g["systemic_risk"] is False
    assert g["systemic_risk_duties"] == []
    arts = [d["article"] for d in g["provider_duties"]]
    assert any("53(1)(a)" in x for x in arts)  # technical documentation
    assert any("53(1)(c)" in x for x in arts)  # copyright policy
    assert any("53(1)(d)" in x for x in arts)  # training data summary


def test_gpai_systemic_risk_above_flop_threshold():
    a = classify(
        {"name": "Frontier", "gpai_model": True, "training_compute_flop": 3e25}
    )
    g = a["gpai_analysis"]
    assert g["systemic_risk"] is True
    assert "1e25" in g["systemic_risk_basis"]
    assert len(g["systemic_risk_duties"]) == len(K.SYSTEMIC_RISK_DUTIES)
    arts = " ".join(d["article"] for d in g["systemic_risk_duties"])
    assert "55(1)(a)" in arts  # adversarial testing
    assert "55(1)(d)" in arts  # cybersecurity


def test_gpai_below_threshold_no_systemic_risk():
    a = classify(
        {"name": "Mid", "gpai_model": True, "training_compute_flop": 5e24}
    )
    assert a["gpai_analysis"]["systemic_risk"] is False


def test_gpai_exactly_at_threshold_no_systemic_risk():
    # Article 51(2): presumption applies when compute is *greater than* 10^25.
    a = classify(
        {"name": "Edge", "gpai_model": True, "training_compute_flop": 1e25}
    )
    assert a["gpai_analysis"]["systemic_risk"] is False


def test_gpai_without_compute_figure_no_presumption():
    a = classify({"name": "Unknown", "gpai_model": True})
    g = a["gpai_analysis"]
    assert g["systemic_risk"] is False
    assert g["training_compute_flop"] is None


def test_gpai_model_can_still_be_high_risk_system():
    # A GPAI model integrated into a high-risk use case: both analyses present.
    a = classify(
        {
            "name": "HireLLM",
            "gpai_model": True,
            "training_compute_flop": 2e25,
            "use_case_tags": ["cv_screening"],
        }
    )
    assert a["risk_tier"] == "high-risk"
    assert a["gpai_analysis"]["systemic_risk"] is True


# --- Conformity checklist ----------------------------------------------------

def test_checklist_covers_section_2_articles():
    items = high_risk_checklist()
    arts = " ".join(c["article"] for c in items)
    for art in ("Article 9", "Article 10", "Article 11", "Article 12",
                "Article 13", "Article 14", "Article 15"):
        assert art in arts, f"{art} missing from checklist"


def test_checklist_includes_registration_and_fria():
    items = high_risk_checklist()
    arts = " ".join(c["article"] for c in items)
    assert "Article 49" in arts  # EU database registration
    assert "Article 27" in arts  # FRIA
    assert "Article 43" in arts  # conformity assessment


def test_checklist_only_for_high_risk():
    assert classify({"name": "chat", "interacts_with_persons": True})[
        "conformity_checklist"] == []
    hr = classify({"name": "hr", "use_case_tags": ["cv_screening"]})
    assert len(hr["conformity_checklist"]) == len(K.HIGH_RISK_CHECKLIST)


def test_every_checklist_item_has_detail():
    for c in high_risk_checklist():
        assert c["item"] and c["detail"] and c["article"]

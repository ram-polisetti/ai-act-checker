"""EU AI Act conformity checker — deterministic risk-tier triage with citations."""

from .classify import classify, EXIT_CODES, TIER_PROHIBITED, TIER_HIGH, TIER_LIMITED, TIER_MINIMAL
from .audit import append_assessment, verify_log

__version__ = "0.1.0"
__all__ = [
    "classify",
    "append_assessment",
    "verify_log",
    "EXIT_CODES",
    "TIER_PROHIBITED",
    "TIER_HIGH",
    "TIER_LIMITED",
    "TIER_MINIMAL",
]

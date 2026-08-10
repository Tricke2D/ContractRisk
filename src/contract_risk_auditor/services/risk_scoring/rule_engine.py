"""
Rule engine for deterministic risk scoring.
"""

from dataclasses import dataclass

from contract_risk_auditor.services.risk_scoring.detectors import CLAUSE_TYPE_DETECTORS


@dataclass
class RuleMatchResult:
    """Result when rule engine finds a match."""

    risk_level: str
    condition_key: str
    confidence: float = 1.0
    scored_by: str = "rule"


def evaluate_rules(
    clause_type: str,
    clause_text: str,
    risk_thresholds: dict,
) -> RuleMatchResult | None:
    """
    Evaluate rules for a clause. Returns RuleMatchResult if rule matches,
    None if no rule matches (fallback to LLM).
    """
    detector = CLAUSE_TYPE_DETECTORS.get(clause_type)
    if detector is None:
        return None

    condition_key = detector(clause_text)
    if condition_key is None:
        return None

    risk_level = risk_thresholds.get(condition_key)
    if risk_level is None:
        return None

    return RuleMatchResult(risk_level=risk_level, condition_key=condition_key)

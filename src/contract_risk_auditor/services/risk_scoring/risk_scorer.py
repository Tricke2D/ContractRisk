"""
Hybrid risk scorer - rule first, LLM fallback.
"""

from dataclasses import dataclass

from contract_risk_auditor.services.llm.ollama_client import OllamaClient
from contract_risk_auditor.services.risk_scoring.rule_engine import evaluate_rules

NEEDS_REVIEW_CONFIDENCE_THRESHOLD = 0.6
HIGH_RISK_CONFIDENCE_THRESHOLD = 0.7


@dataclass
class ClauseRiskResult:
    """Final risk scoring result for one clause."""

    risk_level: str
    confidence: float
    scored_by: str
    reasoning: str
    needs_review: bool


def score_clause_risk(
    clause_type: str,
    clause_text: str,
    standard_language: str,
    risk_thresholds: dict,
    ollama_client: OllamaClient,
) -> ClauseRiskResult:
    """
    Hybrid risk scoring: rule first, LLM fallback.
    """
    # Try rule engine first
    rule_result = evaluate_rules(clause_type, clause_text, risk_thresholds)

    if rule_result is not None:
        return ClauseRiskResult(
            risk_level=rule_result.risk_level,
            confidence=rule_result.confidence,
            scored_by="rule",
            reasoning=f"Detected: condition '{rule_result.condition_key}' matched playbook rule.",
            needs_review=False,
        )

    # Fallback to LLM
    llm_judgment = ollama_client.judge_risk_level(clause_text, standard_language)

    risk_level = llm_judgment["risk_level"]
    confidence = llm_judgment["confidence"]

    # Jika confidence tinggi dan risk_level MEDIUM, upgrade ke HIGH
    if confidence >= HIGH_RISK_CONFIDENCE_THRESHOLD and risk_level == "MEDIUM":
        risk_level = "HIGH"
        reasoning = f"{llm_judgment['reasoning']} (ditingkatkan dari MEDIUM ke HIGH karena confidence tinggi)"
    else:
        reasoning = llm_judgment["reasoning"]

    return ClauseRiskResult(
        risk_level=risk_level,
        confidence=confidence,
        scored_by="llm",
        reasoning=reasoning,
        needs_review=confidence < NEEDS_REVIEW_CONFIDENCE_THRESHOLD,
    )

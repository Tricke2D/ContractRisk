"""
Rule-based risk detectors per clause type.
"""

import re

_UNLIMITED_LIABILITY_PATTERN = re.compile(
    r"\b(unlimited liability|without limitation|no cap on liability|"
    r"shall not be limited|unlimited|no limit|no caps?)\b",
    re.IGNORECASE,
)

_LIABILITY_CAP_MONTHS_PATTERN = re.compile(
    r"fees? paid.{0,40}?(\d+)\s*(?:\(\d+\)\s*)?months?",
    re.IGNORECASE,
)

_NO_NOTICE_REQUIRED_PATTERN = re.compile(
    r"\bautomatically renew\b(?!.{0,150}\bnotice\b)",
    re.IGNORECASE | re.DOTALL,
)

_NOTICE_PERIOD_DAYS_PATTERN = re.compile(
    r"notice.{0,40}?(\d+)\s*(?:\(\d+\)\s*)?days?",
    re.IGNORECASE,
)

_SOLE_DISCRETION_INDEMNITY_PATTERN = re.compile(
    r"\bindemnify.{0,100}?\b(?:sole discretion|unlimited|without limitation)\b",
    re.IGNORECASE | re.DOTALL,
)

_NO_CAP_PATTERN = re.compile(
    r"\b(?:no cap|without limitation|unlimited|not limited)\b",
    re.IGNORECASE,
)


def detect_limitation_of_liability_condition(clause_text: str) -> str | None:
    """Detect condition for limitation_of_liability clause type."""
    # Cek unlimited liability
    if _UNLIMITED_LIABILITY_PATTERN.search(clause_text):
        return "unlimited_liability"

    # Cek no cap
    if _NO_CAP_PATTERN.search(clause_text):
        return "no_cap_mentioned"

    cap_match = _LIABILITY_CAP_MONTHS_PATTERN.search(clause_text)
    if cap_match:
        months = int(cap_match.group(1))
        return "cap_12_months_fee_or_more" if months >= 12 else "cap_below_6_months_fee"

    return "no_cap_mentioned"  # Default jika tidak ada cap yang jelas


def detect_auto_renewal_condition(clause_text: str) -> str | None:
    """Detect condition for auto_renewal clause type."""
    if _NO_NOTICE_REQUIRED_PATTERN.search(clause_text):
        return "no_notice_period_required"

    notice_match = _NOTICE_PERIOD_DAYS_PATTERN.search(clause_text)
    if notice_match:
        days = int(notice_match.group(1))
        return "notice_period_30_days_or_more" if days >= 30 else "notice_period_under_30_days"

    return None


def detect_indemnification_condition(clause_text: str) -> str | None:
    """Detect condition for indemnification clause type."""
    if _SOLE_DISCRETION_INDEMNITY_PATTERN.search(clause_text):
        return "one_sided_sole_discretion_indemnity"

    # Cek unlimited indemnity
    if _UNLIMITED_LIABILITY_PATTERN.search(clause_text):
        return "unlimited_indemnity"

    return None


def detect_termination_condition(clause_text: str) -> str | None:
    """Detect condition for termination clause type."""
    if "without notice" in clause_text.lower() or "immediate termination" in clause_text.lower():
        return "termination_without_notice"

    notice_match = _NOTICE_PERIOD_DAYS_PATTERN.search(clause_text)
    if notice_match:
        days = int(notice_match.group(1))
        if days < 30:
            return "notice_period_under_30_days"

    return None


def detect_confidentiality_condition(clause_text: str) -> str | None:
    """Detect condition for confidentiality clause type."""
    # Cek duration
    year_match = re.search(r"(\d+)\s*(?:\(\d+\)\s*)?years?", clause_text, re.IGNORECASE)
    if year_match:
        years = int(year_match.group(1))
        if years < 3:
            return "less_than_3_years"
        return "3_years_or_more"

    # No confidentiality obligation
    if "no confidentiality" in clause_text.lower() or "not confidential" in clause_text.lower():
        return "no_confidentiality_obligation"

    return None


CLAUSE_TYPE_DETECTORS = {
    "limitation_of_liability": detect_limitation_of_liability_condition,
    "auto_renewal": detect_auto_renewal_condition,
    "indemnification": detect_indemnification_condition,
    "termination": detect_termination_condition,
    "confidentiality": detect_confidentiality_condition,
}

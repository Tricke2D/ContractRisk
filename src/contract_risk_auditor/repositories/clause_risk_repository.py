"""
Clause risk repository - data access for clause_risks table.
"""

from decimal import Decimal

from sqlalchemy.orm import Session

from contract_risk_auditor.domain.models.clause import Clause
from contract_risk_auditor.domain.models.clause_risk import ClauseRisk


class ClauseRiskRepository:
    """Data access for clause_risks."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create_clause_risk(
        self,
        clause_id: str,
        risk_level: str,
        deviation_reason: str,
        matched_playbook_standard_id: str | None = None,
        confidence_score: float | None = None,
        scored_by: str = "llm",
        needs_review: bool = False,
    ) -> ClauseRisk:
        """Create a new clause risk entry."""
        risk = ClauseRisk(
            clause_id=clause_id,
            risk_level=risk_level,
            deviation_reason=deviation_reason,
            matched_playbook_standard_id=matched_playbook_standard_id,
            confidence_score=Decimal(str(confidence_score))
            if confidence_score is not None
            else None,
            scored_by=scored_by,
            needs_review=needs_review,
        )
        self._session.add(risk)
        self._session.commit()
        self._session.refresh(risk)
        return risk

    def get_risks_by_clause(self, clause_id: str) -> list[ClauseRisk]:
        """Get all risks for a clause."""
        return self._session.query(ClauseRisk).filter(ClauseRisk.clause_id == clause_id).all()

    def get_high_risk_by_contract(self, contract_id: str) -> list[ClauseRisk]:
        """Get all HIGH risk clauses for a contract."""
        return (
            self._session.query(ClauseRisk)
            .join(Clause, ClauseRisk.clause_id == Clause.id)
            .filter(Clause.contract_id == contract_id)
            .filter(ClauseRisk.risk_level == "HIGH")
            .all()
        )

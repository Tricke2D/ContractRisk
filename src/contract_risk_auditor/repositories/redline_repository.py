"""
Redline repository - data access for redline_suggestions table.
"""

from sqlalchemy.orm import Session

from contract_risk_auditor.domain.models.redline_suggestion import RedlineSuggestion


class RedlineRepository:
    """Data access for redline_suggestions."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create_redline(
        self,
        clause_id: str,
        suggested_replacement_text: str,
        rationale: str,
        variant_label: str = "assertive",
        status: str = "DRAFT",
    ) -> RedlineSuggestion:
        """Create a new redline suggestion."""
        redline = RedlineSuggestion(
            clause_id=clause_id,
            suggested_replacement_text=suggested_replacement_text,
            rationale=rationale,
            variant_label=variant_label,
            status=status,
        )
        self._session.add(redline)
        self._session.commit()
        self._session.refresh(redline)
        return redline

    def update_status(self, redline_id: str, status: str, reviewer_note: str | None = None) -> dict:
        """Update redline status."""
        redline = self._session.get(RedlineSuggestion, redline_id)
        if redline:
            redline.status = status
            if reviewer_note:
                redline.reviewer_note = reviewer_note
            self._session.commit()
            return {"id": redline_id, "status": status}
        return {"error": "Redline not found"}

    def get_by_clause(self, clause_id: str) -> list[RedlineSuggestion]:
        """Get all redlines for a clause."""
        return (
            self._session.query(RedlineSuggestion)
            .filter(RedlineSuggestion.clause_id == clause_id)
            .all()
        )

    def get_by_contract(self, contract_id: str) -> list[RedlineSuggestion]:
        """Get all redlines for a contract."""
        return (
            self._session.query(RedlineSuggestion)
            .join(RedlineSuggestion.clause)
            .filter(RedlineSuggestion.contract_id == contract_id)
            .all()
        )

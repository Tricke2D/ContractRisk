"""
Clause repository - data access for clauses table.
"""

from sqlalchemy.orm import Session

from contract_risk_auditor.domain.models.clause import Clause


class ClauseRepository:
    """Data access for clauses."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create_clause(
        self,
        contract_id: str,
        clause_text: str,
        section_number: str | None = None,
        clause_type: str | None = None,
        page_number: int | None = None,
    ) -> Clause:
        """Create a new clause entry."""
        clause = Clause(
            contract_id=contract_id,
            section_number=section_number,
            clause_text=clause_text,
            clause_type=clause_type,
            page_number=page_number,
        )
        self._session.add(clause)
        self._session.commit()
        self._session.refresh(clause)
        return clause

    def get_clause(self, clause_id: str) -> Clause | None:
        """Get a clause by ID."""
        return self._session.get(Clause, clause_id)

    def get_clauses_by_contract(self, contract_id: str) -> list[Clause]:
        """Get all clauses for a contract."""
        return self._session.query(Clause).filter(Clause.contract_id == contract_id).all()

    def get_clauses_by_type(self, clause_type: str, limit: int = 100) -> list[Clause]:
        """Get clauses by type."""
        return (
            self._session.query(Clause).filter(Clause.clause_type == clause_type).limit(limit).all()
        )

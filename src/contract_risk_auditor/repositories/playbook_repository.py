"""
Playbook repository - data access for playbook_standards table.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from contract_risk_auditor.domain.models.playbook_standard import PlaybookStandard


class PlaybookRepository:
    """Data access for playbook_standards."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create_standard(
        self,
        clause_type: str,
        standard_language: str,
        risk_thresholds: dict,
    ) -> PlaybookStandard:
        """Create a new playbook standard entry."""
        standard = PlaybookStandard(
            clause_type=clause_type,
            standard_language=standard_language,
            risk_thresholds=risk_thresholds,
        )
        self._session.add(standard)
        self._session.commit()
        self._session.refresh(standard)
        return standard

    def get_standard(self, standard_id: str) -> PlaybookStandard | None:
        """Get a playbook standard by ID."""
        return self._session.get(PlaybookStandard, standard_id)

    def update_embedding(self, playbook_standard_id: str, embedding_vector: list[float]) -> None:
        """Update embedding vector for a playbook standard."""
        standard = self._session.get(PlaybookStandard, playbook_standard_id)
        if standard:
            standard.standard_embedding = embedding_vector
            self._session.commit()

    def find_most_similar_standard(
        self,
        clause_type: str,
        clause_embedding: list[float],
        top_k: int = 1,
    ) -> list[PlaybookStandard]:
        """Find most similar playbook standard using cosine similarity."""
        # Simplified: since we're using custom Vector type,
        # we'll do a simple query without pgvector similarity for now
        query = select(PlaybookStandard).where(PlaybookStandard.clause_type == clause_type)
        results = self._session.execute(query).scalars().all()
        return results[:top_k] if results else []

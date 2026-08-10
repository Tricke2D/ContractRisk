"""
Clause risk ORM model.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from contract_risk_auditor.core.database import Base


class ClauseRisk(Base):  # type: ignore[misc]
    __tablename__ = "clause_risks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clause_id = Column(
        UUID(as_uuid=True), ForeignKey("clauses.id", ondelete="CASCADE"), nullable=False
    )
    risk_level = Column(String(10), nullable=False)
    deviation_reason = Column(Text, nullable=True)
    similarity_score_to_standard = Column(Numeric(5, 4), nullable=True)
    matched_playbook_standard_id = Column(
        UUID(as_uuid=True), ForeignKey("playbook_standards.id"), nullable=True
    )
    confidence_score = Column(Numeric(5, 4), nullable=True)
    scored_by = Column(String(10), nullable=False, server_default="llm")
    needs_review = Column(Boolean, nullable=False, server_default="false")  # ← Fix ini
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    __table_args__ = (CheckConstraint("risk_level IN ('LOW', 'MEDIUM', 'HIGH')"),)

    clause = relationship("Clause", back_populates="risks")

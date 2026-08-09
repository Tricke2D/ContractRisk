"""
Redline suggestion ORM model.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from contract_risk_auditor.core.database import Base


class RedlineSuggestion(Base):
    __tablename__ = "redline_suggestions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clause_id = Column(UUID(as_uuid=True), ForeignKey("clauses.id", ondelete="CASCADE"), nullable=False)
    suggested_replacement_text = Column(Text, nullable=False)
    rationale = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    clause = relationship("Clause", backref="redline_suggestions")
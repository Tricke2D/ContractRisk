"""
Playbook standard ORM model.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID, VECTOR

from contract_risk_auditor.core.config import settings
from contract_risk_auditor.core.database import Base


class PlaybookStandard(Base):
    __tablename__ = "playbook_standards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clause_type = Column(String(100), nullable=False)
    standard_language = Column(Text, nullable=False)
    risk_thresholds = Column(JSON, nullable=False, default={})
    standard_embedding = Column(VECTOR(settings.embedding_dimension), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
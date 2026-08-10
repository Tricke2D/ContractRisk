"""
Contract ORM model.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from contract_risk_auditor.core.database import Base


class Contract(Base):  # type: ignore[misc]
    __tablename__ = "contracts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False)
    party_name = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    clauses = relationship("Clause", back_populates="contract", cascade="all, delete-orphan")

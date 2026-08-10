"""
Playbook standard ORM model with pgvector support.
"""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Column, DateTime, String, Text, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID

from contract_risk_auditor.core.config import settings
from contract_risk_auditor.core.database import Base


class Vector(TypeDecorator):
    """
    PostgreSQL vector type for pgvector extension.
    Stores list[float] as string in database.
    """

    impl = Text
    cache_ok = True

    def __init__(self, dimension: int = 768) -> None:
        self.dimension = dimension
        super().__init__()

    def load_dialect_impl(self, dialect: Any) -> Any:
        return dialect.type_descriptor(Text())

    def process_bind_param(self, value: list[float] | None, dialect: Any) -> str | None:
        if value is None:
            return None
        return "[" + ",".join(str(v) for v in value) + "]"

    def process_result_value(self, value: str | None, dialect: Any) -> list[float] | None:
        if value is None:
            return None
        # Remove brackets and split
        cleaned = value.strip("[]")
        if not cleaned:
            return []
        return [float(x) for x in cleaned.split(",")]


class PlaybookStandard(Base):  # type: ignore[misc]
    __tablename__ = "playbook_standards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clause_type = Column(String(100), nullable=False)
    standard_language = Column(Text, nullable=False)
    risk_thresholds = Column(JSON, nullable=False, default={})
    standard_embedding = Column(Vector(settings.embedding_dimension), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

"""
Add risk scoring columns to clause_risks
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("clause_risks", sa.Column("matched_playbook_standard_id", UUID(), nullable=True))
    op.add_column("clause_risks", sa.Column("confidence_score", sa.Numeric(5, 4), nullable=True))
    op.add_column(
        "clause_risks", sa.Column("scored_by", sa.String(10), nullable=False, server_default="llm")
    )
    op.add_column(
        "clause_risks",
        sa.Column("needs_review", sa.Boolean(), nullable=False, server_default="false"),
    )


def downgrade() -> None:
    op.drop_column("clause_risks", "needs_review")
    op.drop_column("clause_risks", "scored_by")
    op.drop_column("clause_risks", "confidence_score")
    op.drop_column("clause_risks", "matched_playbook_standard_id")

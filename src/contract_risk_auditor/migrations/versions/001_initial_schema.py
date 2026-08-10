"""
Initial schema for Contract Risk Auditor
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSON, UUID

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # contracts
    op.create_table(
        "contracts",
        sa.Column(
            "id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("party_name", sa.String(255), nullable=False),
        sa.Column(
            "uploaded_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    # clauses
    op.create_table(
        "clauses",
        sa.Column(
            "id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column(
            "contract_id",
            UUID(as_uuid=True),
            sa.ForeignKey("contracts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("section_number", sa.String(64), nullable=True),
        sa.Column("clause_text", sa.Text(), nullable=False),
        sa.Column("clause_type", sa.String(100), nullable=True),
        sa.Column("page_number", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index("idx_clauses_contract_id", "clauses", ["contract_id"])
    op.create_index("idx_clauses_clause_type", "clauses", ["clause_type"])

    # playbook_standards
    op.create_table(
        "playbook_standards",
        sa.Column(
            "id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("clause_type", sa.String(100), nullable=False),
        sa.Column("standard_language", sa.Text(), nullable=False),
        sa.Column("risk_thresholds", JSON, nullable=False, server_default="{}"),
        sa.Column("standard_embedding", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    # clause_risks
    op.create_table(
        "clause_risks",
        sa.Column(
            "id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column(
            "clause_id",
            UUID(as_uuid=True),
            sa.ForeignKey("clauses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("risk_level", sa.String(10), nullable=False),
        sa.Column("deviation_reason", sa.Text(), nullable=True),
        sa.Column("similarity_score_to_standard", sa.Numeric(5, 4), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.CheckConstraint("risk_level IN ('LOW', 'MEDIUM', 'HIGH')"),
    )
    op.create_index("idx_clause_risks_clause_id", "clause_risks", ["clause_id"])

    # redline_suggestions
    op.create_table(
        "redline_suggestions",
        sa.Column(
            "id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column(
            "clause_id",
            UUID(as_uuid=True),
            sa.ForeignKey("clauses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("suggested_replacement_text", sa.Text(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    op.drop_table("redline_suggestions")
    op.drop_table("clause_risks")
    op.drop_table("playbook_standards")
    op.drop_table("clauses")
    op.drop_table("contracts")

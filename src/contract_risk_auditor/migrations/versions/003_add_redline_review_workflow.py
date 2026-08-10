"""
Add redline review workflow columns.
"""

import sqlalchemy as sa
from alembic import op

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "redline_suggestions",
        sa.Column("variant_label", sa.String(20), nullable=False, server_default="assertive"),
    )
    op.add_column(
        "redline_suggestions",
        sa.Column("status", sa.String(20), nullable=False, server_default="DRAFT"),
    )
    op.add_column(
        "redline_suggestions",
        sa.Column("reviewer_note", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("redline_suggestions", "reviewer_note")
    op.drop_column("redline_suggestions", "status")
    op.drop_column("redline_suggestions", "variant_label")

"""create ticket tables

Revision ID: 20260611_0001
Revises:
Create Date: 2026-06-11
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260611_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "tickets",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("customer_id", sa.String(length=100), nullable=True),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_tickets_customer_id", "tickets", ["customer_id"])
    op.create_index("ix_tickets_source", "tickets", ["source"])
    op.create_index("ix_tickets_status", "tickets", ["status"])

    op.create_table(
        "ticket_predictions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("ticket_id", sa.Uuid(), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("category_confidence", sa.Float(), nullable=False),
        sa.Column("sentiment", sa.String(length=50), nullable=False),
        sa.Column("sentiment_confidence", sa.Float(), nullable=False),
        sa.Column("priority", sa.String(length=50), nullable=False),
        sa.Column("priority_confidence", sa.Float(), nullable=False),
        sa.Column("model_version", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["ticket_id"], ["tickets.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ticket_predictions_category", "ticket_predictions", ["category"])
    op.create_index("ix_ticket_predictions_priority", "ticket_predictions", ["priority"])
    op.create_index("ix_ticket_predictions_sentiment", "ticket_predictions", ["sentiment"])
    op.create_index("ix_ticket_predictions_ticket_id", "ticket_predictions", ["ticket_id"])


def downgrade() -> None:
    op.drop_index("ix_ticket_predictions_ticket_id", table_name="ticket_predictions")
    op.drop_index("ix_ticket_predictions_sentiment", table_name="ticket_predictions")
    op.drop_index("ix_ticket_predictions_priority", table_name="ticket_predictions")
    op.drop_index("ix_ticket_predictions_category", table_name="ticket_predictions")
    op.drop_table("ticket_predictions")
    op.drop_index("ix_tickets_status", table_name="tickets")
    op.drop_index("ix_tickets_source", table_name="tickets")
    op.drop_index("ix_tickets_customer_id", table_name="tickets")
    op.drop_table("tickets")

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.ticket import Ticket


def utc_now() -> datetime:
    return datetime.now(UTC)


class TicketPrediction(Base):
    __tablename__ = "ticket_predictions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    ticket_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tickets.id"), index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    category_confidence: Mapped[float] = mapped_column(Float, nullable=False)
    sentiment: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    sentiment_confidence: Mapped[float] = mapped_column(Float, nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    priority_confidence: Mapped[float] = mapped_column(Float, nullable=False)
    model_version: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    ticket: Mapped[Ticket] = relationship(back_populates="predictions")

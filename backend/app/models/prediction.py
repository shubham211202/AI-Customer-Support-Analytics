from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.models.base import TimestampMixin


class Prediction(TimestampMixin, Base):
    __tablename__ = "predictions"

    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id"),
        unique=True,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    sentiment: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    category_confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    priority_confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    sentiment_confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    ticket = relationship(
        "Ticket",
        back_populates="prediction",
    )
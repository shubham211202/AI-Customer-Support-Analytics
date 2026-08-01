from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.models.base import TimestampMixin


class Ticket(TimestampMixin, Base):
    __tablename__ = "tickets"

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String(50),
        default="web",
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="open",
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        String(30),
        default="medium",
        nullable=False,
    )

    # Relationships

    customer = relationship(
        "Customer",
        back_populates="tickets",
    )

    prediction = relationship(
        "Prediction",
        back_populates="ticket",
        uselist=False,
        cascade="all, delete-orphan",
    )
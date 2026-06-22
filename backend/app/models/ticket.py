from sqlalchemy import Column, Integer, String, Text, ForeignKey

from app.database.session import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    subject = Column(String, nullable=False)
    description = Column(Text)

    status = Column(String, default="open")
    priority = Column(String, default="medium")

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )
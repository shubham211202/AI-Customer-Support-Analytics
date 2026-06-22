from sqlalchemy import Column, Integer, String, Float, ForeignKey

from app.database.session import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id"),
        nullable=False
    )

    sentiment = Column(String, nullable=False)
    category = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
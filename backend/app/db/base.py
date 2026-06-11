from app.db.session import Base
from app.models.prediction import TicketPrediction
from app.models.ticket import Ticket

__all__ = ["Base", "Ticket", "TicketPrediction"]

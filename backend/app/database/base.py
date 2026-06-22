from app.database.session import Base

from app.models.customer import Customer
from app.models.ticket import Ticket
from app.models.prediction import Prediction
from app.models.user import User

__all__ = [
    "Base",
    "Customer",
    "Ticket",
    "Prediction",
    "User",
]
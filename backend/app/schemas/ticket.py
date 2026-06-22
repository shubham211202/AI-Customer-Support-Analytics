from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict

from app.schemas.prediction import PredictionRead


class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class TicketPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class TicketCategory(str, Enum):
    billing = "billing"
    technical = "technical"
    account = "account"
    general = "general"


class TicketSentiment(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"


class TicketCreate(BaseModel):
    customer_id: int
    subject: str
    description: str
    source: str


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


class TicketRead(BaseModel):
    id: int
    customer_id: int
    subject: str
    description: str
    source: str
    status: str
    prediction: PredictionRead | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TicketListResponse(BaseModel):
    items: list[TicketRead]
    limit: int
    offset: int
    total: int
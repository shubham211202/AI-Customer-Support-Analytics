import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.prediction import PredictionRead

TicketSource = Literal["email", "chat", "web", "phone"]
TicketStatus = Literal["open", "in_progress", "resolved", "closed"]
TicketCategory = Literal["billing", "technical_issue", "account_access", "refund", "general_query"]
TicketSentiment = Literal["positive", "neutral", "negative"]
TicketPriority = Literal["low", "medium", "high", "urgent"]


class TicketCreate(BaseModel):
    customer_id: str | None = Field(default=None, max_length=100)
    subject: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=10)
    source: TicketSource


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


class TicketRead(BaseModel):
    id: uuid.UUID
    customer_id: str | None
    subject: str
    description: str
    source: TicketSource
    status: TicketStatus
    prediction: PredictionRead | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TicketListResponse(BaseModel):
    items: list[TicketRead]
    limit: int
    offset: int
    total: int

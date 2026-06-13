import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PredictionCreate(BaseModel):
    category: str
    category_confidence: float = Field(ge=0, le=1)
    sentiment: str
    sentiment_confidence: float = Field(ge=0, le=1)
    priority: str
    priority_confidence: float = Field(ge=0, le=1)
    model_version: str | None = None


class PredictionRead(BaseModel):
    id: uuid.UUID
    category: str
    category_confidence: float = Field(ge=0, le=1)
    sentiment: str
    sentiment_confidence: float = Field(ge=0, le=1)
    priority: str
    priority_confidence: float = Field(ge=0, le=1)
    model_version: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

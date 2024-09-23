# app/schemas/message.py
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class UrgencyLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class MessageCreate(BaseModel):
    content: str
    urgency: UrgencyLevel

class MessageResponse(BaseModel):
    id: int
    content: str
    urgency: UrgencyLevel
    created_by_id: int
    created_at: datetime
    reply: str | None

    class Config:
        from_attributes = True

class MessageReply(BaseModel):
    reply: str


from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from enum import Enum as PyEnum


class UrgencyLevel(str, PyEnum):
    low = "low"
    medium = "medium"
    high = "high"

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    created_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    urgency = Column(Enum(UrgencyLevel), default=UrgencyLevel.low, nullable=False)
    reply = Column(String, nullable=True)  

    created_by = relationship("User", backref="messages")

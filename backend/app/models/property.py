# app/models/property.py
from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    number_of_houses = Column(Integer)
    description = Column(Text)

    def __repr__(self):
        return f"<Property(name={self.name}, location={self.location})>"
